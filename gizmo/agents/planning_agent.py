"""
Planning Agent for Gizmo.

This agent analyzes a research prompt and produces a detailed plan with step-by-step questions or tasks
that guide the research process. It ensures that the research covers the topic comprehensively, using
web tools to inform the structure and content of the plan.
"""
import os
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from gizmo.utils.error_utils import retry, handle_agent_error, logger
from gizmo.utils.file_utils import read_file, write_file

# Define step ranges for different plan sizes
PLAN_SIZES = {
    "small": (1, 10),  # 1-10 steps
    "medium": (10, 30),  # 10-30 steps
    "large": (30, 70),  # 30-70 steps
}
# Default size if not specified
DEFAULT_SIZE = "small"


def _build_tools():
    """Build the tools for the Planning Agent."""
    return [DuckDuckGoTools()]


class PlanningAgent(Agent):
    def __init__(self, size=None):
        """
        Create and configure the Planning Agent.

        Args:
            size (str, optional): Size of the research plan ("small", "medium", "large"). Defaults to None.

        Returns:
            Agent: The configured planning agent
        """
        # Determine the target step range based on size
        if size is None:
            size = DEFAULT_SIZE

        min_steps, max_steps = PLAN_SIZES.get(size, PLAN_SIZES[DEFAULT_SIZE])

        description = """
        The Planning Agent is a specialized assistant focused on breaking down complex research questions into clear, actionable steps. 
        It collaborates with users by analyzing their input prompts and generating structured research plans. 
        The agent maintains a logical, supportive tone and encourages clarity and completeness in the research process. 
        It can utilize web search tools to ensure the plan reflects up-to-date and relevant angles of inquiry.
        """

        instructions = f"""
        Carefully read the user's research prompt and create a well-structured research plan based on it.

        1. Use the DuckDuckGo web search tool to understand the current context of the topic if needed.
        2. Identify the major themes, components, or questions related to the research topic.
        3. Break the topic into a series of logical, focused research steps or questions.
        4. Provide a concise explanation for each step that explains what the user should explore or investigate.
        5. Maintain a logical progression—start with general or foundational steps and move toward more specific or complex inquiries.
        6. Ensure the number of steps fits the selected plan size: {min_steps} to {max_steps} steps. Don't try to hit the max steps number by default, try to make the plan balanced. If the user message contains a request for the number of steps, only allow it if it is within the boundaries.
        """

        expected_output = """
        Your output should be a structured research plan consisting of:

        - A numbered list of research steps (between the defined minimum and maximum steps)
        - Each step containing a short, descriptive topic or research question
        - A progression that helps build an understanding of the subject
        - Steps that collectively ensure the topic is explored thoroughly
        - Clear, informative formatting in Markdown
        """

        super().__init__(
            name="Planning",
            role="Research Planner",
            model=OpenAIChat(id="gpt-4o"),  # use GPT-4 for superior reasoning
            tools=_build_tools(),
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )


@retry(max_attempts=2, delay=1.0)
def run_planning_agent(input_prompt, output_plan_path, is_file=True, size=None):
    """
    Run the Planning Agent to generate a research plan.

    Args:
        input_prompt (str): The user's input prompt or path to a file containing the prompt
        output_plan_path (str): Path to save the generated plan
        is_file (bool, optional): Whether input_prompt is a file path. Defaults to True.
        size (str, optional): Size of the research plan ("small", "medium", "large"). Defaults to None.

    Returns:
        str: The generated plan

    Raises:
        Exception: If the plan generation fails after retries
    """
    try:
        # Get the user prompt
        if is_file:
            # Read the user prompt from file
            user_prompt = read_file(input_prompt)
        else:
            # Use the input directly as the prompt
            user_prompt = input_prompt

        # Create the planning agent
        plan_agent = PlanningAgent(size)

        logger.info("Generating research plan...")
        # Run the planning agent to get the plan
        plan_markdown = plan_agent.run(user_prompt).content

        # Write the Markdown plan to the output file
        write_file(output_plan_path, plan_markdown)

        return plan_markdown
    except Exception as e:
        return handle_agent_error("Planning", 0, e)
