"""
Workflow orchestration for Gizmo.

This module implements the core workflow for Gizmo, including:
1. Planning phase - Generate a research plan from a prompt
2. Research phase - Execute a multi-agent research workflow based on a plan
"""

import os

from gizmo.agents.crawler_agent import create_crawler_agent
from gizmo.agents.planning_agent import create_planning_agent
from gizmo.agents.researcher_agent import create_researcher_agent
from gizmo.agents.summarizer_agents import create_step_summarizer_agent, create_final_summarizer_agent
from gizmo.agents.writer_agent import create_writer_agent
from gizmo.utils.error_utils import retry, handle_agent_error, log_error
from gizmo.utils.file_utils import read_file, write_file, ensure_dir, parse_plan_file, formulate_search_query


@retry(max_attempts=3, delay=2.0)
def run_plan(input_prompt, output_plan_path, is_file=True):
    """
    Generate a research plan from a prompt.

    Args:
        input_prompt (str): Path to the input prompt file or the prompt text itself
        output_plan_path (str): Path to save the output plan
        is_file (bool, optional): Whether input_prompt is a file path. Defaults to True.

    Returns:
        str: The generated plan

    Raises:
        Exception: If the plan generation fails after retries
    """
    # Get the user prompt
    if is_file:
        # Read the user prompt from file
        user_prompt = read_file(input_prompt)
    else:
        # Use the input directly as the prompt
        user_prompt = input_prompt

    # Create the planning agent
    plan_agent = create_planning_agent()

    print("Generating research plan...")
    # Run the planning agent to get the plan
    plan_markdown = plan_agent.run(user_prompt).content

    # Write the plan to the output file
    write_file(output_plan_path, plan_markdown)

    return plan_markdown


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
        step_num = f"step{i}"
        print(f"\nProcessing {step_num}: {step}")

        try:
            # Step 1: Crawler - Search the web for information
            print(f"  Running crawler for {step_num}...")
            search_results = run_crawler_agent(step, i, memory_dir)

            # Step 2: Researcher - Analyze the information
            print(f"  Running researcher for {step_num}...")
            analysis = run_researcher_agent(step, search_results, i, memory_dir)

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


@retry(max_attempts=2, delay=1.0)
def run_crawler_agent(step, step_number, memory_dir):
    """
    Run the Crawler Agent for a step.

    Args:
        step (str): The step description
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files

    Returns:
        str: The search results

    Raises:
        Exception: If the crawler agent fails after retries
    """
    try:
        # Create the crawler agent
        crawler = create_crawler_agent()

        # Formulate a search query from the step
        query = formulate_search_query(step)

        # Run the crawler agent
        search_results = crawler.run(f"Research question: {query}")

        # Save the search results
        search_file = os.path.join(memory_dir, f"step{step_number}_search.md")
        write_file(search_file, search_results)

        return search_results
    except Exception as e:
        return handle_agent_error("Crawler", step_number, e)


@retry(max_attempts=2, delay=1.0)
def run_researcher_agent(step, search_results, step_number, memory_dir):
    """
    Run the Researcher Agent for a step.

    Args:
        step (str): The step description
        search_results (str): The search results from the crawler
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files

    Returns:
        str: The analysis

    Raises:
        Exception: If the researcher agent fails after retries
    """
    try:
        # Create the researcher agent
        researcher = create_researcher_agent()

        # Prepare the input for the researcher
        researcher_input = (
            f"# Research Question\n\n{step}\n\n"
            f"# Reference Information\n\n{search_results}"
        )

        # Run the researcher agent
        analysis = researcher.run(researcher_input)

        # Save the analysis
        analysis_file = os.path.join(memory_dir, f"step{step_number}_analysis.md")
        write_file(analysis_file, analysis)

        return analysis
    except Exception as e:
        return handle_agent_error("Researcher", step_number, e, search_results)


@retry(max_attempts=2, delay=1.0)
def run_writer_agent(analysis, step_number, output_dir):
    """
    Run the Writer Agent for a step.

    Args:
        analysis (str): The analysis from the researcher
        step_number (int): The step number
        output_dir (str): Directory to save output files

    Returns:
        str: The polished report

    Raises:
        Exception: If the writer agent fails after retries
    """
    try:
        # Create the writer agent
        writer = create_writer_agent()

        # Run the writer agent
        polished_report = writer.run(analysis)

        # Save the polished report
        report_file = os.path.join(output_dir, f"step{step_number}.md")
        write_file(report_file, polished_report)

        return polished_report
    except Exception as e:
        fallback = analysis  # Use the researcher's analysis as fallback
        write_file(os.path.join(output_dir, f"step{step_number}.md"), fallback)
        return handle_agent_error("Writer", step_number, e, fallback)


@retry(max_attempts=2, delay=1.0)
def run_step_summarizer_agent(polished_report, step_number, memory_dir):
    """
    Run the Step Summarizer Agent for a step.

    Args:
        polished_report (str): The polished report from the writer
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files

    Returns:
        str: The summary

    Raises:
        Exception: If the step summarizer agent fails after retries
    """
    try:
        # Create the step summarizer agent
        summarizer = create_step_summarizer_agent()

        # Run the step summarizer agent
        summary = summarizer.run(polished_report)

        # Save the summary
        summary_file = os.path.join(memory_dir, f"step{step_number}_summary.md")
        write_file(summary_file, summary)

        return summary
    except Exception as e:
        # Generate a simple summary as fallback
        fallback = f"This step covered: {polished_report[:100]}..."
        write_file(os.path.join(memory_dir, f"step{step_number}_summary.md"), fallback)
        return handle_agent_error("Step Summarizer", step_number, e, fallback)


@retry(max_attempts=2, delay=1.0)
def run_final_summarizer_agent(step_summaries, output_dir):
    """
    Run the Final Summarizer Agent.

    Args:
        step_summaries (list): List of step summaries
        output_dir (str): Directory to save output files

    Returns:
        str: The final summary

    Raises:
        Exception: If the final summarizer agent fails after retries
    """
    try:
        # Create the final summarizer agent
        summarizer = create_final_summarizer_agent()

        # Prepare the input for the final summarizer
        summarizer_input = "# Research Step Summaries\n\n" + "\n\n".join(step_summaries)

        # Run the final summarizer agent
        final_summary = summarizer.run(summarizer_input)

        # Save the final summary
        summary_file = os.path.join(output_dir, "summary_final.md")
        write_file(summary_file, final_summary)

        return final_summary
    except Exception as e:
        # Generate a simple summary as fallback
        fallback = "# Research Summary\n\n" + "\n\n".join(step_summaries)
        write_file(os.path.join(output_dir, "summary_final.md"), fallback)
        return handle_agent_error("Final Summarizer", 0, e, fallback)
