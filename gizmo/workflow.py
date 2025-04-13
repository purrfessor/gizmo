"""
Workflow orchestration for Gizmo.

This module implements the core workflow for Gizmo, including:
1. Planning phase - Generate a research plan from a prompt
2. Research phase - Execute a multi-agent research workflow based on a plan

The workflow includes:
1. Direct inclusion of the research plan in the researcher agent's instructions
2. A research toolkit that allows the researcher agent to:
   a. Read results from previous research steps
   b. Find relevant information from previous steps
"""

import os
import time

from gizmo.agents.planning_agent import run_planning_agent
from gizmo.agents.researcher_agent import run_researcher_agent
from gizmo.agents.source_agent import run_source_agent
from gizmo.agents.summarizer_agents import run_step_summarizer_agent, run_final_summarizer_agent
from gizmo.agents.writer_agent import run_writer_agent
from gizmo.utils.error_utils import retry, log_error, logger, set_step_context, clear_step_context
from gizmo.utils.file_utils import write_file, ensure_dir, parse_plan_file
from gizmo.utils.metrics_utils import UsageAccumulator


@retry(max_attempts=3, delay=2.0)
def run_plan(input_prompt, output_plan_path, is_file=True, step_number=None):
    """
    Generate a research plan from a prompt.

    Args:
        input_prompt (str): Path to the input prompt file or the prompt text itself
        output_plan_path (str): Path to save the output plan
        is_file (bool, optional): Whether input_prompt is a file path. Defaults to True.
        step_number (int, optional): Target number of steps for the research plan. Defaults to None.

    Returns:
        str: The generated plan

    Raises:
        Exception: If the plan generation fails after retries
    """
    logger.info("Generating research plan...")
    return run_planning_agent(input_prompt, output_plan_path, is_file, step_number)


def run_research(plan_path, output_dir, memory_dir=".memory"):
    """
    Execute a research workflow based on a plan.

    Args:
        plan_path (str): Path to the plan file
        output_dir (str): Directory to save the output files
        memory_dir (str): Directory to save intermediate files

    Raises:
        Exception: If the research execution fails
    """
    # Start timing the entire research process
    research_start_time = time.time()

    # Create a usage accumulator to track metrics across all agent runs
    usage_accumulator = UsageAccumulator()

    # Ensure directories exist
    ensure_dir(memory_dir)
    ensure_dir(output_dir)

    # Parse the plan file to get the list of steps
    steps = parse_plan_file(plan_path)

    logger.info(f"Parsed {len(steps)} research steps from plan")

    # Store step summaries for the final summary
    step_summaries = []

    # Process each step in the plan
    for i, step in enumerate(steps, start=1):
        step_num = f"step #{i}"
        # Set the step context for logging
        set_step_context(i)
        logger.info(f"Processing {step_num}: {step}")
        step_start_time = time.time()

        try:
            # Step 1: Source - Search the web for information
            logger.info(f"Running source agent...")
            source_start_time = time.time()
            source_response = run_source_agent(step, i, memory_dir)
            usage_accumulator.record(source_response)
            source_time = time.time() - source_start_time
            search_results = source_response

            # Log source agent metrics if available
            logger.info(f"Source agent completed in {source_time:.2f}s")

            # Step 2: Researcher - Analyze the information
            logger.info(f"Running researcher...")
            researcher_start_time = time.time()
            researcher_response = run_researcher_agent(step, search_results, i, memory_dir, output_dir, plan_path)
            usage_accumulator.record(researcher_response)
            researcher_time = time.time() - researcher_start_time
            analysis = researcher_response

            # Log researcher agent metrics if available
            logger.info(f"Researcher agent completed in {researcher_time:.2f}s")

            # Step 3: Writer - Polish the analysis
            logger.info(f"Running writer...")
            writer_start_time = time.time()
            writer_response = run_writer_agent(analysis, i, output_dir)
            usage_accumulator.record(writer_response)
            writer_time = time.time() - writer_start_time
            polished_report = writer_response

            # Log writer agent metrics if available
            logger.info(f"Writer agent completed in {writer_time:.2f}s")

            # Step 4: Step Summarizer - Summarize the step
            logger.info(f"Running step summarizer...")
            summarizer_start_time = time.time()
            summarizer_response = run_step_summarizer_agent(polished_report, i, memory_dir)
            usage_accumulator.record(summarizer_response)
            summarizer_time = time.time() - summarizer_start_time
            summary = summarizer_response

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
            final_summary_response = run_final_summarizer_agent(step_summaries, output_dir)
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
