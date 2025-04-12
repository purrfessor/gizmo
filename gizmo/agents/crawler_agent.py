"""
Crawler Agent for Gizmo.

This module defines the Crawler Agent, which is responsible for fetching
information from the web relevant to a given research step.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


def create_crawler_agent():
    """Create and configure the Crawler Agent."""
    return Agent(
        name="Crawler",
        role="Web Searcher",
        model=OpenAIChat(id="gpt-3.5-turbo"),  # faster, cheaper model
        tools=[DuckDuckGoTools()],
        instructions=(
            "You are a web search agent. Your task is to find relevant information for the given research question.\n"
            "Use DuckDuckGo to search for information on the given topic.\n"
            "Return the most relevant results (with brief snippets) that relate to the query.\n"
            "Include the source URLs for each result.\n"
            "Format your response as a Markdown list with clear headings for each source.\n"
            "Focus on finding diverse and reliable sources that provide comprehensive information."
        ),
        markdown=True
    )