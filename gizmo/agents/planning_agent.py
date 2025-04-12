"""
Planning Agent for Gizmo.

This module defines the Planning Agent, which is responsible for analyzing
the user's input prompt and producing a Markdown-formatted plan listing
all research steps or questions.
"""
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field

# Cap the step number at 30 regardless of input
max_steps = 50
# Default step limit if not specified
default_steps = 15

class ResearchStep(BaseModel):
    step: int = Field(..., description="Step number")
    topic: str = Field(..., description="Provide step details: what needs to be done, what needs to be researched, what information needs to be provided.")

class Plan(BaseModel):
    steps: List[ResearchStep] = Field(..., description="Provide research steps list.")

def create_planning_agent(step_number=None):
    """
    Create and configure the Planning Agent.

    Args:
        step_number (int, optional): Target number of steps for the research plan. Defaults to None.

    Returns:
        Agent: Configured planning agent
    """

    # Determine the target number of steps
    if step_number is not None and step_number > 0:
        target_steps = min(step_number, max_steps)
    else:
        target_steps = default_steps

    return Agent(
        name="Planning Agent",
        role="Research Planner",
        model=OpenAIChat(id="gpt-4o"),  # use GPT-4 for superior reasoning
        tools=[DuckDuckGoTools()],     # allows web search if needed
        instructions=(
            "Analyze the user's research query and devise a structured plan.\n"
            "It is preferable to use the web search to fetch the recent information to build the plan.\n"
            "Break the problem into clear, answerable research questions or steps.\n"
            "Each step should be focused on a specific aspect of the research topic.\n"
            "Include a brief description for each step explaining what should be researched.\n"
            "Ensure the steps are logically ordered and comprehensive.\n"
            f"Try to create approximately {target_steps} steps in your plan.\n"
            f"The upper limit for the number of steps is {max_steps}."
        ),
        structured_outputs=True,
        response_model=Plan,
        markdown=True
    )
