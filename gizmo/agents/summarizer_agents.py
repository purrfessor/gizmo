"""
Summarizer Agents for Gizmo.

This module defines two summarizer agents:
1. Step Summarizer Agent - Produces a concise summary of each step's findings
2. Final Summarizer Agent - Generates a final summary of the entire research project
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat


def create_step_summarizer_agent():
    """Create and configure the Step Summarizer Agent."""
    return Agent(
        name="Step Summarizer",
        role="Summarizer",
        model=OpenAIChat(id="gpt-3.5-turbo"),  # efficient for summarization
        tools=[],  # no external tools needed
        instructions=(
            "You are a summarizer. Your task is to create concise summaries of research content.\n"
            "Summarize the following text in a few sentences, capturing the main point and any important findings.\n"
            "Be concise and clear, focusing on the key insights and conclusions.\n"
            "Your summary should be no more than 3-5 sentences or a short paragraph.\n"
            "Ensure that the most important facts and findings are preserved in your summary."
        ),
        markdown=True
    )


def create_final_summarizer_agent():
    """Create and configure the Final Summarizer Agent."""
    return Agent(
        name="Final Summarizer",
        role="Synthesizer",
        model=OpenAIChat(id="gpt-4o"),  # better for synthesis across multiple topics
        tools=[],  # no external tools needed
        instructions=(
            "You are a research synthesizer. Your task is to create a comprehensive summary of an entire research project.\n"
            "Given the summaries of each step of the research, produce an overall summary of the findings.\n"
            "This summary should address the original query broadly and highlight key insights from each part of the research.\n"
            "Structure your summary with an introduction, key findings section, and conclusion.\n"
            "You may use bullet points for separate themes if necessary.\n"
            "Keep it concise but comprehensive, focusing on the most significant insights and their implications.\n"
            "Your summary should provide a complete picture of what was learned through the research."
        ),
        markdown=True
    )