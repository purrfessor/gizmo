"""
Researcher Agent for Gizmo.

This module defines the Researcher Agent, which is responsible for taking
the raw info from the crawler and producing an in-depth analysis or
explanation for that step.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from gizmo.utils.research_toolkit import ResearchToolkit
from gizmo.utils.file_utils import read_file

def create_researcher_agent(output_dir=None, memory_dir=None, plan_path=None):
    """
    Create and configure the Researcher Agent.

    Args:
        output_dir (str, optional): Directory containing the output files
        memory_dir (str, optional): Directory containing the memory files
        plan_path (str, optional): Path to the plan file

    Returns:
        Agent: The configured researcher agent
    """
    # Create tools list with DuckDuckGo search
    tools = [DuckDuckGoTools()]

    # Add research toolkit if directories are provided
    if output_dir and memory_dir:
        research_toolkit = ResearchToolkit(output_dir, memory_dir, plan_path)
        tools.append(research_toolkit)

    # Base instructions for the researcher agent
    base_instructions = (
        "You are a research analyst. Your task is to analyze information and produce a detailed report.\n"
        "Using the reference information provided and any necessary web searches, "
        "write a detailed, well-structured answer for the topic/question given.\n"
        "Cite facts as needed and ensure the answer is comprehensive.\n"
        "You may perform additional searches if the provided information is insufficient.\n"
        "Structure your response with clear headings, subheadings, and bullet points where appropriate.\n"
        "Include citations to sources where relevant.\n"
        "Be thorough and ensure all aspects of the question are addressed.\n"
        "Your analysis should be factual, balanced, and in-depth.\n\n"
    )

    # Add the research plan to the instructions if available
    plan_instructions = ""
    if plan_path and os.path.exists(plan_path):
        plan_content = read_file(plan_path)
        plan_instructions = (
            f"# Research Plan\n\n"
            f"{plan_content}\n\n"
            f"IMPORTANT: Always consider this research plan when conducting your analysis.\n"
        )

    # Add instructions about using the toolkit for previous research results
    toolkit_instructions = (
        "Use the ResearchToolkit to access previous step results that may be relevant to your current task."
    )

    # Combine all instructions
    full_instructions = base_instructions + plan_instructions + toolkit_instructions

    return Agent(
        name="Researcher",
        role="Analyst",
        model=OpenAIChat(id="gpt-4o"),  # advanced reasoning model
        tools=tools,
        instructions=full_instructions,
        markdown=True
    )
