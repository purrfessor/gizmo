"""
Source Agent for Gizmo.

This module defines the Source Agent, which is responsible for fetching
information from the web relevant to a given research step.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from gizmo.utils.error_utils import retry, handle_agent_error
from gizmo.utils.file_utils import write_file
import os


def _build_tools():
    """Build the tools for the Source Agent."""
    return [DuckDuckGoTools()]


class SourceAgent(Agent):
    def __init__(self):
        """
        Create and configure the Source Agent.

        Returns:
            Agent: The configured source agent
        """
        
        description = """
            The Source Agent is a specialized web search assistant designed to find relevant information 
            for research questions. It operates efficiently to gather diverse and reliable sources from 
            the web, providing well-formatted results that can be used for further analysis.
        """

        instructions = """
            You are a web search agent. Your task is to find relevant information for the given research question.
            Use DuckDuckGo to search for information on the given topic.
            Return the most relevant results (with brief snippets) that relate to the query.
            Include the source URLs for each result.
            Format your response as a Markdown list with clear headings for each source.
            Focus on finding diverse and reliable sources that provide comprehensive information.
        """

        expected_output = """
            Your output should be a well-formatted Markdown document containing:
            
            - A list of relevant sources with clear headings
            - Brief snippets or summaries of the key information from each source
            - The complete URL for each source
            - A diverse range of perspectives and information types
            - Information that directly addresses the research question
        """

        super().__init__(
            name="Source",
            role="Web Searcher",
            model=OpenAIChat(id="gpt-3.5-turbo"),  # faster, cheaper model
            tools=_build_tools(),
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )


@retry(max_attempts=2, delay=1.0)
def run_source_agent(step, step_number, memory_dir):
    """
    Run the Source Agent for a step.

    Args:
        step (str): The step description
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files

    Returns:
        str: The search results

    Raises:
        Exception: If the source agent fails after retries
    """
    try:
        # Create the source agent
        source = SourceAgent()

        # Formulate a search query from the step
        from gizmo.utils.file_utils import formulate_search_query
        query = formulate_search_query(step)

        # Run the source agent
        search_results = source.run(f"Research question: {query}").content

        # Save the search results
        search_file = os.path.join(memory_dir, f"step{step_number}_search.md")
        write_file(search_file, search_results)

        return search_results
    except Exception as e:
        return handle_agent_error("Source", step_number, e)