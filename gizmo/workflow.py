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

import json
import os

from gizmo.agents.researcher_agent import run_researcher_agent
from gizmo.agents.source_agent import run_source_agent
from gizmo.agents.planning_agent import run_planning_agent
from gizmo.agents.summarizer_agents import run_step_summarizer_agent, run_final_summarizer_agent
from gizmo.agents.writer_agent import run_writer_agent
from gizmo.utils.error_utils import retry, handle_agent_error, log_error
from gizmo.utils.file_utils import read_file, write_file, ensure_dir, parse_plan_file, formulate_search_query


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
    print("Generating research plan...")
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
    # Ensure directories exist
    ensure_dir(memory_dir)
    ensure_dir(output_dir)

    # Parse the plan file to get the list of steps
    steps = parse_plan_file(plan_path)

    print(f"Parsed {len(steps)} research steps from plan")

    # Store step summaries for the final summary
    step_summaries = []

    # Process each step in the plan
    for i, step in enumerate(steps, start=1):
        step_num = f"step #{i}"
        print(f"\nProcessing {step_num}: {step}")

        try:
            # Step 1: Source - Search the web for information
            print(f"  Running source agent for {step_num}...")
            search_results = run_source_agent(step, i, memory_dir)

            # Step 2: Researcher - Analyze the information
            print(f"  Running researcher for {step_num}...")
            analysis = run_researcher_agent(step, search_results, i, memory_dir, output_dir, plan_path)

            # Step 3: Writer - Polish the analysis
            print(f"  Running writer for {step_num}...")
            polished_report = run_writer_agent(analysis, i, output_dir)

            # Step 4: Step Summarizer - Summarize the step
            print(f"  Running step summarizer for {step_num}...")
            summary = run_step_summarizer_agent(polished_report, i, memory_dir)

            # Store the summary for the final summary
            step_summaries.append(f"## Step {i}: {step}\n\n{summary}")

        except Exception as e:
            error_msg = f"Error processing step {i}: {str(e)}"
            print(f"  {error_msg}")
            log_error(e, error_msg)

            # Create error files
            error_content = f"# Error in Step {i}: {step}\n\n{str(e)}"
            write_file(os.path.join(output_dir, f"{step_num}.md"), error_content)
            write_file(os.path.join(memory_dir, f"{step_num}_summary.md"), "Error: " + str(e))

            # Add error to summaries
            step_summaries.append(f"## Step {i}: {step}\n\nError: {str(e)}")

    # Final step: Generate the overall summary
    if step_summaries:
        print("\nGenerating final summary...")
        try:
            run_final_summarizer_agent(step_summaries, output_dir)
        except Exception as e:
            error_msg = f"Error generating final summary: {str(e)}"
            print(f"  {error_msg}")
            log_error(e, error_msg)

            # Create error file for summary
            error_content = f"# Error in Final Summary\n\n{str(e)}"
            write_file(os.path.join(output_dir, "summary_final.md"), error_content)

    print("\nResearch completed!")






