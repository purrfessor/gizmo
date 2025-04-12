"""
Writer Agent for Gizmo.

This module defines the Writer Agent, which is responsible for taking
the researcher's output and rewriting or polishing it for clarity,
style, and coherence.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat


def create_writer_agent():
    """Create and configure the Writer Agent."""
    return Agent(
        name="Writer",
        role="Refiner",
        model=OpenAIChat(id="gpt-3.5-turbo"),  # language polish model
        tools=[],  # no external tools needed
        instructions=(
            "You are a technical writer. Your task is to refine and polish content.\n"
            "Rewrite and polish the given content into a clear, well-structured Markdown document.\n"
            "Improve fluency and fix any grammatical issues, but do not change factual content.\n"
            "Use headings, bullet points, or tables where appropriate to enhance readability.\n"
            "Ensure the document has a professional tone and flows logically.\n"
            "Maintain all citations and references from the original text.\n"
            "Focus on clarity, coherence, and readability while preserving all information."
        ),
        markdown=True
    )