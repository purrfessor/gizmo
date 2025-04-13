"""
Plan Parser Agent for Gizmo.

This agent reads a plan.md file and produces a structured JSON output that can be used for iteration.
"""
import json
import os
import re
from pydoc import describe
from typing import List, Dict

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field

from gizmo.utils.error_utils import retry, handle_agent_error, logger
from gizmo.utils.file_utils import read_file, write_file

class Step(BaseModel):
    step: int = Field(..., description="The step number.")
    topic: str = Field(..., description="The topic of the step: what topic is going to be researched.")

class Plan(BaseModel):
    steps: List[Step]


class PlanParserAgent(Agent):
    def __init__(self):
        """
        Create and configure the Plan Parser Agent.

        Returns:
            Agent: The configured plan parser agent
        """
        description = """
        The Plan Parser Agent is a Markdown interpreter designed to read research plans and cleanly reformat them. 
        It takes loosely structured plan content and rewrites it as a clear, numbered Markdown list that is logically ordered and well-formatted. 
        The tone is simple, structured, and focused on clarity and consistency.
        """

        instructions = """
        Your job is to take a rough or loosely written research plan and return a clean, numbered Markdown list of steps.

        1. Identify each research step from the input (they may be numbered, bulleted, or written as sentences).
        2. Normalize the format into a properly numbered Markdown list.
        3. Use the content of each step as is, don't modify it in any way.
        4. Ensure logical ordering and consistent tone across all steps.
        5. Do not return JSON or unstructured text—return only the formatted Markdown plan.
        """

        expected_output = """
        Your output should be a numbered list that:

        - Clearly outlines each step of the research plan
        - Maintains the original meaning and order of the steps
        - Has no extra commentary or unstructured text
        """

        super().__init__(
            name="PlanParser",
            role="Plan Parser",
            model=OpenAIChat(id="gpt-4o"),  # use GPT-4 for superior reasoning
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            response_model=Plan,
            structured_outputs=True
        )


@retry(max_attempts=2, delay=1.0)
def run_plan_parser_agent(plan):
    """
    Run the Plan Parser Agent to read the .md plan.

    Args:
        plan (str): Research plan

    Returns:
        Plan: The parsed plan

    Raises:
        Exception: If the plan parsing fails after retries
    """
    try:
        # Create the plan parser agent
        parser_agent = PlanParserAgent()

        logger.info("Parsing research plan...")
        # Run the plan parser agent to get the structured output
        return parser_agent.run(plan)
    except Exception as e:
        return handle_agent_error("PlanParser", 0, e)