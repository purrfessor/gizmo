"""
Writer Agent for Gizmo.

This module defines the Writer Agent, which is responsible for taking
the researcher's output and rewriting or polishing it for clarity,
style, and coherence.
"""
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from gizmo.utils.error_utils import retry, handle_agent_error
from gizmo.utils.file_utils import write_file


class WriterAgent(Agent):
    def __init__(self):
        """
        Create and configure the Writer Agent.

        Returns:
            Agent: The configured writer agent
        """

        description = """
            The Writer Agent is a specialized editing assistant designed to refine and polish content.
            It improves the clarity, structure, and readability of technical content while preserving
            all factual information and maintaining the original meaning.
        """

        instructions = """
            You are a technical writer. Your task is to refine and polish content.
            Rewrite and polish the given content into a clear, well-structured Markdown document.
            Improve fluency and fix any grammatical issues, but do not change factual content.
            Use headings, bullet points, or tables where appropriate to enhance readability.
            Ensure the document has a professional tone and flows logically.
            Maintain all citations and references from the original text.
            Focus on clarity, coherence, and readability while preserving all information.
        """

        expected_output = """
            Your output should be a polished Markdown document that:

            - Has improved clarity, structure, and readability
            - Maintains all factual content from the original
            - Uses appropriate formatting (headings, bullet points, tables) to enhance readability
            - Has a professional tone and logical flow
            - Preserves all citations and references
            - Is free of grammatical errors and awkward phrasing
        """

        super().__init__(
            name="Writer",
            role="Refiner",
            model=OpenAIChat(id="gpt-3.5-turbo"),  # language polish model
            tools=[],  # no external tools needed
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )


@retry(max_attempts=2, delay=1.0)
def run_writer_agent(analysis, step_number, output_dir):
    """
    Run the Writer Agent for a step.

    Args:
        analysis (str): The analysis from the researcher
        step_number (int): The step number
        output_dir (str): Directory to save output files

    Returns:
        str: The polished report

    Raises:
        Exception: If the writer agent fails after retries
    """
    try:
        # Create the writer agent
        writer = WriterAgent()
        from gizmo.utils.error_utils import logger

        # Run the writer agent
        response = writer.run(analysis)

        # Save the polished report
        report_file = os.path.join(output_dir, f"step{step_number}.md")
        write_file(report_file, response.content)

        return response
    except Exception as e:
        fallback = analysis  # Use the researcher's analysis as fallback
        write_file(os.path.join(output_dir, f"step{step_number}.md"), fallback)
        return handle_agent_error("Writer", step_number, e, fallback)
