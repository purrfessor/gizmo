"""
Researcher Agent for Gizmo.

This module defines the Researcher Agent, which is responsible for taking
the raw info from the source agent and producing an in-depth analysis or
explanation for that step.
"""
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools

from gizmo.tools.research_toolkit import ResearchContextToolkit
from gizmo.utils.error_utils import retry, handle_agent_error
from gizmo.utils.file_utils import read_file, write_file


def _build_tools(output_dir, memory_dir, plan_path):
    tools = [DuckDuckGoTools(), ArxivTools()]

    # Add research toolkit if directories are provided
    if output_dir and memory_dir:
        research_toolkit = ResearchContextToolkit(output_dir, memory_dir, plan_path)
        tools.append(research_toolkit)

    return tools


class ResearcherAgent(Agent):
    def __init__(self, output_dir=None, memory_dir=None, plan_path=None):
        """
            Create and configure the Researcher Agent.

            Args:
                output_dir (str, optional): Directory containing the output files
                memory_dir (str, optional): Directory containing the memory files
                plan_path (str, optional): Path to the plan file

            Returns:
                Agent: The configured researcher agent
            """

        description = """
            The Researcher Agent is a highly capable analytical assistant designed to help users investigate complex topics, synthesize information, and produce comprehensive written analyses. 
            It operates with a formal, balanced, and objective tone, while remaining approachable and clear. 
            The agent interacts with the user by interpreting their research request, using available tools to gather relevant information, and presenting structured and insightful findings. 
            It can utilize previous research outputs as context and may perform live searches to supplement its knowledge when necessary.
        """

        instructions = f"""
            You are a research analyst assigned to conduct thorough investigations based on user queries or topics. Follow these steps for every task:

                1. Understand the user's question or topic. Clarify ambiguities before proceeding.
                2. Search for relevant information using the DuckDuckGo search tool if the links provided in the initial prompt are not enough.
                3. Read articles on Arxiv if the data found already is not enough and you need scientific knowledge.
                4. Review provided research plan and incorporate it into your strategy.
                5. If you find any related topics in the research plan, use the ResearchToolkit to access previously stored results or ongoing project data.
                6. Collect and evaluate all information critically, checking sources and consistency.
                7. Structure your findings logically, using clear headings and bullet points where needed.
                8. Provide factual, unbiased, and in-depth explanations.
                9. Cite your sources or indicate where data originated, especially if it's retrieved through a tool.
                10. Ensure your response addresses all key aspects of the query and provides actionable insight.
        """

        expected_output = """
            Your output should be a clear, well-organized, and detailed research report or analytical response. It must include:

                - A structured format with headings and subheadings.
                - Concise summaries supported by bullet points where appropriate.
                - In-depth coverage of the topic with clear, factual explanations.
                - Direct references or citations to the sources used.
                - Consideration of any provided research plan.
                - Thoughtful conclusions or recommendations, where applicable.

            Avoid speculation unless clearly stated, and ensure your language is professional, neutral, and precise.
        """

        super().__init__(
            name="Researcher",
            role="Analyst",
            model=OpenAIChat(id="gpt-4o"),  # we need an advanced reasoning model for this task
            tools=_build_tools(output_dir, memory_dir, plan_path),
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )

@retry(max_attempts=2, delay=1.0)
def run_researcher_agent(step, search_results, step_number, memory_dir, output_dir, plan_path=None):
    """
    Run the Researcher Agent for a step.

    Args:
        step (str): The step description
        search_results (str): The search results from the source agent
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files
        output_dir (str): Directory containing the output files
        plan_path (str, optional): Path to the plan file

    Returns:
        str: The analysis

    Raises:
        Exception: If the researcher agent fails after retries
    """
    try:
        # Create the researcher agent with access to research toolkit
        researcher = ResearcherAgent(output_dir, memory_dir, plan_path)
        from gizmo.utils.error_utils import logger

        # Prepare the input for the researcher
        researcher_input = (
            f"# Research Question\n\n{step}\n\n"
            f"# Reference Information\n\n{search_results}\n\n"
        )

        if plan_path:
            researcher_input += f"# General research plan\n\n{read_file(plan_path)}\n\n"

        # Run the researcher agent
        response = researcher.run(researcher_input)

        # Save the analysis
        analysis_file = os.path.join(memory_dir, f"step{step_number}_analysis.md")
        write_file(analysis_file, response.content)

        return response
    except Exception as e:
        return handle_agent_error("Researcher", step_number, e, search_results)
