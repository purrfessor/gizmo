"""
GPT Researcher Agent for Gizmo.

This module defines the GPT Researcher Agent, which is responsible for using
the gpt-researcher library to produce comprehensive research on a topic.
"""
import os
from typing import List

from gpt_researcher import GPTResearcher

from gizmo.utils.error_utils import retry, logger
from gizmo.utils.file_utils import write_file


class GPTResearcherError(Exception):
    """Exception raised for errors in the GPT Researcher."""
    pass


@retry(max_attempts=2, delay=1.0)
async def run_gpt_researcher_agent(
    topic: str, 
    step_number: int, 
    output_dir: str, 
    plan: str, 
    previous_steps_summaries: List[str]=None,
    initial_query: str=None,
    source_urls: List[str]=None
) -> str:
    """
    Run the GPT Researcher Agent for a step.

    Args:
        topic (str): The research topic
        step_number (int): The step number
        output_dir (str): Directory to save output files
        plan (str): The research plan
        previous_steps_summaries (List[str]): The accumulated summaries of all previous research steps as a list.
                                             Each item is a formatted summary of a previous step.
        initial_query (str): The initial query of the research
        source_urls (List[str]): List of URLs to use as sources for the research

    Returns:
        str: The research report

    Raises:
        GPTResearcherError: If the GPT Researcher fails
    """

    query = f"""
        <task>
            You are an AI deep research assistant. You are performing a step in a bigger research. You need to make a research on the given topic. Always keep the initial query in mind throughout your research process.
        </task>

        <researchTopic>
            {topic}
        </researchTopic>
    """

    context = f"""
        <currentStepNumber>
            {step_number}
        </currentStepNumber>

        <initialQuery>
            {initial_query or "Unavailable."}
        </initialQuery>

        <researchPlan>
            {plan}
        </researchPlan>
    """

    # Initialize the researcher with source URLs if available
    researcher = GPTResearcher(
        query=query, 
        report_type="deep", 
        context=context,
        source_urls=source_urls or []
    )
    
    # Join the list into a string for compatibility with GPTResearcher
    report = await researcher.write_report(relevant_written_contents=previous_steps_summaries or [])
    research_costs = researcher.get_costs()

    step_result_file = os.path.join(output_dir, f"step{step_number}.md")
    write_file(step_result_file, report)

    logger.info(f"GPT Researcher costs: {research_costs:.4f}$")

    return report
