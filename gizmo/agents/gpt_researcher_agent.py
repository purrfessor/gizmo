"""
GPT Researcher Agent for Gizmo.

This module defines the GPT Researcher Agent, which is responsible for using
the gpt-researcher library to produce comprehensive research on a topic.
"""
import os
import subprocess
import json
import tempfile
from typing import Dict, Any, Optional

from gpt_researcher import GPTResearcher

from gizmo.utils.error_utils import retry, handle_agent_error, logger
from gizmo.utils.file_utils import read_file, write_file, ensure_dir


class GPTResearcherError(Exception):
    """Exception raised for errors in the GPT Researcher."""
    pass


@retry(max_attempts=2, delay=1.0)
def run_gpt_researcher_agent(topic: str, step_number: int, memory_dir: str, output_dir: str, plan: str, previous_steps_summaries: str) -> str:
    """
    Run the GPT Researcher Agent for a step.

    Args:
        topic (str): The research topic
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files
        output_dir (str): Directory to save output files
        plan (str): The research plan
        previous_steps_summaries (str): The short summaries of the previous research steps results

    Returns:
        str: The research report

    Raises:
        GPTResearcherError: If the GPT Researcher fails
    """

    query = f"""
        <task>
            You are an AI deep research assistant. You are performing a step in a bigger research. You need to make a research on the given topic.
        </task>
    
        <researchTopic>
            {topic}
        </researchTopic>
        
        <currentStepNumber>
            {step_number}
        </currentStepNumber>
        
        <researchPlan>
            {plan}
        </researchPlan>
        
        <previousStepsSummaries>
            {previous_steps_summaries}
        </previousStepsSummaries>
    """

    researcher = GPTResearcher(query = query, report_type="research_report") # "deep"

    research_result = researcher.conduct_research()
    report = researcher.write_report()

    research_context = researcher.get_research_context()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()

    return """
        Yay!
    """


