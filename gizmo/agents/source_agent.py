"""
Source Agent for Gizmo.

This agent conducts targeted web searches to support specific research steps. It returns curated lists
of relevant, diverse, and reliable sources, each accompanied by summaries and links. The goal is to
enrich the research process with high-quality external content.
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from gizmo.utils.error_utils import retry, handle_agent_error
from gizmo.utils.file_utils import write_file


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
        The Source Agent is a focused web search assistant that helps gather relevant external content to support individual research steps. 
        It interacts with research prompts by conducting real-time web searches using DuckDuckGo and returning a curated list of sources. 
        The agent maintains an efficient, informative, and neutral tone while prioritizing source diversity and relevance.
        """

        instructions = """
        You are a web search assistant supporting a specific research step. For each request:

        1. Interpret the research question or prompt carefully.
        2. Use the DuckDuckGo tool to find the most relevant, reliable, and diverse sources.
        3. Summarize the key insights from each result using a short, informative snippet.
        4. Provide a clean, well-formatted Markdown list that includes:
           - A heading for each source or article
           - A brief summary/snippet
           - The full URL

        Focus on quality over quantity and ensure each result adds meaningful value to the research topic.
        """

        expected_output = """
        Your output should be a well-organized Markdown list that includes:

        - Clear source headings or titles
        - Short summaries or highlights for each item
        - Full source URLs
        - Diverse viewpoints and reliable references
        - Only content that directly helps answer or explore the research step

        Format your list cleanly and avoid clutter or unrelated content.
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
        from gizmo.utils.error_utils import logger
        query = formulate_search_query(step)

        # Run the source agent
        response = source.run(f"Research question: {query}")

        # Save the search results
        search_file = os.path.join(memory_dir, f"step{step_number}_search.md")
        write_file(search_file, response.content)

        return response
    except Exception as e:
        return handle_agent_error("Source", step_number, e)
