"""
Deep workflow implementation for Gizmo.

This module implements the deep research workflow for Gizmo, including:
1. Planning phase - Generate a research plan from a prompt
2. Deep research phase - Execute a deep research workflow using GPT Researcher

The workflow includes:
1. Direct inclusion of the research plan in the researcher agent's instructions
2. Use of GPT Researcher for deep research
"""

import os
import time

from gizmo.agents.gpt_researcher_agent import run_gpt_researcher_agent
from gizmo.agents.plan_parser_agent import run_plan_parser_agent
from gizmo.agents.planning_agent import run_planning_agent
from gizmo.agents.summarizer_agents import run_step_summarizer_agent, run_final_summarizer_agent
from gizmo.utils.error_utils import retry, log_error, logger, set_step_context, clear_step_context
from gizmo.utils.file_utils import write_file, ensure_dir, read_file
from gizmo.utils.metrics_utils import UsageAccumulator
from gizmo.workflows.workflow_base import GizmoWorkflow


class DeepGizmoWorkflow(GizmoWorkflow):
    """
    Deep implementation of the Gizmo workflow.

    This class implements the deep research workflow with the following steps:
    1. Planning phase - Generate a research plan from a prompt
    2. Deep research phase - Execute a deep research workflow using GPT Researcher
    """

    @retry(max_attempts=3, delay=2.0)
    def run_plan(self, input_prompt, output_plan_path, is_file=True, size=None):
        """
        Generate a research plan from a prompt and parse it into structured format.

        Args:
            input_prompt (str): Path to the input prompt file or the prompt text itself
            output_plan_path (str): Path to save the output plan
            is_file (bool, optional): Whether input_prompt is a file path. Defaults to True.
            size (str, optional): Size of the research plan ("small", "medium", "large"). Defaults to None.

        Returns:
            str: The generated plan

        Raises:
            Exception: If the plan generation fails after retries
        """
        # Generate the plan in markdown format
        return run_planning_agent(input_prompt, output_plan_path, is_file, size)

    async def run_research(self, plan_path, output_dir, memory_dir=".memory", deep=True, initial_input=None):
        """
        Execute a deep research workflow based on a plan.

        Args:
            plan_path (str): Path to the plan file
            output_dir (str): Directory to save the output files
            memory_dir (str): Directory to save intermediate files
            deep (bool): Whether to use GPT Researcher for deep research
            initial_input (str, optional): Initial input for the research

        Raises:
            Exception: If the research execution fails
        """
        # Set default retriever to duckduckgo if not already set
        if "RETRIEVER" not in os.environ:
            os.environ["RETRIEVER"] = "duckduckgo"

        # Start timing the entire research process
        research_start_time = time.time()

        # Create a usage accumulator to track metrics across all agent runs
        usage_accumulator = UsageAccumulator()

        # Ensure directories exist
        ensure_dir(memory_dir)
        ensure_dir(output_dir)

        # Parse the plan file to get the list of steps
        logger.info("Reading research plan...")
        plan = read_file(plan_path)
        parsed_plan = run_plan_parser_agent(plan)
        usage_accumulator.record(parsed_plan)
        steps = parsed_plan.content.steps

        logger.info(f"Parsed {len(steps)} research steps from plan")

        # Store step summaries for the final summary
        step_summaries = []

        # Process each step in the plan
        for step in enumerate(steps, start=1):
            i = step[1].step
            topic = step[1].topic
            step_num = f"step #{i}"
            # Set the step context for logging
            set_step_context(i)
            logger.info(f"Processing {step_num}: {step}")
            step_start_time = time.time()

            try:
                if not deep:
                    # This workflow only handles deep research
                    raise ValueError("Regular research is not supported by DeepGizmoWorkflow")
                else:
                    # Use GPT Researcher for deep research
                    logger.info(f"Running GPT Researcher for deep research...")
                    deep_research_start_time = time.time()
                    research_report = await run_gpt_researcher_agent(topic, i, memory_dir, output_dir, plan, '\n\n'.join(step_summaries), initial_input)
                    deep_research_time = time.time() - deep_research_start_time

                    # Log GPT Researcher metrics
                    logger.info(f"GPT Researcher completed in {deep_research_time:.2f}s")

                    # Step Summarizer - Summarize the step
                    logger.info(f"Running step summarizer...")
                    summarizer_start_time = time.time()
                    summarizer_response = run_step_summarizer_agent(research_report, i, memory_dir)
                    usage_accumulator.record(summarizer_response)
                    summarizer_time = time.time() - summarizer_start_time
                    summary = summarizer_response.content

                    # Log summarizer agent metrics if available
                    logger.info(f"Step summarizer agent completed in {summarizer_time:.2f}s")

                    # Store the summary for the final summary
                    step_summaries.append(f"## Step {i}: {step}\n\n{summary}")

                # Log total step metrics
                step_time = time.time() - step_start_time
                logger.info(f"Step completed in {step_time:.2f}s total")

            except Exception as e:
                error_msg = f"Error processing step {i}: {str(e)}"
                logger.error(f"{error_msg}")
                log_error(e, error_msg)

                # Create error files
                error_content = f"# Error in Step {i}: {step}\n\n{str(e)}"
                write_file(os.path.join(output_dir, f"step{i}.md"), error_content)
                write_file(os.path.join(memory_dir, f"step{i}_summary.md"), "Error: " + str(e))

                # Add error to summaries
                step_summaries.append(f"## Step {i}: {step}\n\nError: {str(e)}")

            finally:
                # Clear the step context after processing
                clear_step_context()

        # Final step: Generate the overall summary
        if step_summaries:
            logger.info("Generating final summary...")
            final_summary_start_time = time.time()
            try:
                run_final_summarizer_agent(step_summaries, output_dir)
                final_summary_time = time.time() - final_summary_start_time

                # Log final summarizer metrics if available
                logger.info(f"Final summarizer completed in {final_summary_time:.2f}s")

            except Exception as e:
                error_msg = f"Error generating final summary: {str(e)}"
                logger.error(f"{error_msg}")
                log_error(e, error_msg)

                # Create error file for summary
                error_content = f"# Error in Final Summary\n\n{str(e)}"
                write_file(os.path.join(output_dir, "summary_final.md"), error_content)

        # Calculate and log total research metrics
        total_research_time = time.time() - research_start_time
        logger.info(f"Research completed in {total_research_time:.2f}s total!")
        logger.info(f"Total steps processed: {len(steps)}")

        # Log accumulated metrics
        metrics = usage_accumulator.get_metrics()
        logger.info(f"Total tokens used: {metrics['total_tokens']}")
        logger.info(f"Total model time: {metrics['model_time']:.4f}s")


# Create a global instance of the DeepGizmoWorkflow
deep_workflow = DeepGizmoWorkflow()
