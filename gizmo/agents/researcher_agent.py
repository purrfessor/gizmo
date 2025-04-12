"""
Researcher Agent for Gizmo.

This module defines the Researcher Agent, which is responsible for taking
the raw info from the crawler and producing an in-depth analysis or
explanation for that step.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


def create_researcher_agent():
    """Create and configure the Researcher Agent."""
    return Agent(
        name="Researcher",
        role="Analyst",
        model=OpenAIChat(id="gpt-4o"),  # advanced reasoning model
        tools=[DuckDuckGoTools()],     # can search the web further
        instructions=(
            "You are a research analyst. Your task is to analyze information and produce a detailed report.\n"
            "Using the reference information provided and any necessary web searches, "
            "write a detailed, well-structured answer for the topic/question given.\n"
            "Cite facts as needed and ensure the answer is comprehensive.\n"
            "You may perform additional searches if the provided information is insufficient.\n"
            "Structure your response with clear headings, subheadings, and bullet points where appropriate.\n"
            "Include citations to sources where relevant.\n"
            "Be thorough and ensure all aspects of the question are addressed.\n"
            "Your analysis should be factual, balanced, and in-depth."
        ),
        markdown=True,
        show_tool_calls=True  # show tool calls during development
    )