"""
Planning Agent for Gizmo.

This module defines the Planning Agent, which is responsible for analyzing
the user's input prompt and producing a Markdown-formatted plan listing
all research steps or questions.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


def create_planning_agent():
    """Create and configure the Planning Agent."""
    return Agent(
        name="Planning Agent",
        role="Research Planner",
        model=OpenAIChat(id="gpt-4o"),  # use GPT-4 for superior reasoning
        tools=[DuckDuckGoTools()],     # allows web search if needed
        instructions=(
            "Analyze the user's research query and devise a structured plan.\n"
            "Break the problem into clear, answerable research questions or steps.\n"
            "Output the plan as a numbered list of steps in Markdown.\n"
            "Each step should be focused on a specific aspect of the research topic.\n"
            "Include a brief description for each step explaining what should be researched.\n"
            "Ensure the steps are logically ordered and comprehensive.\n"
            "The upper limit for the number of steps is 15."
        ),
        markdown=True
    )