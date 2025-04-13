"""
Writer Agent for Gizmo.

This module defines the Writer Agent, which takes the researcher's output and rewrites or polishes it
for clarity, coherence, structure, and readability. It ensures technical content is presented cleanly
and professionally without altering meaning or facts.
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
        The Writer Agent is a specialized editorial assistant responsible for refining the researcher's output. 
        It enhances clarity, coherence, and style while preserving the original meaning and factual accuracy. 
        The agent writes in a professional, structured, and readable tone, improving grammar, flow, and formatting.
        The agent also uses mermaid diagrams for illustrating the data provided when necessary. 
        """

        instructions = """
        You are a professional technical writer and editor.

        1. Review the provided content carefully.
        2. Rewrite and polish the text to improve clarity, grammar, and logical flow.
        3. Maintain the original meaning and all factual information.
        4. Use Markdown formatting to enhance structure and readability (e.g., with headings, bullet points, or tables).
        5. Ensure a professional and polished tone throughout.
        6. Do not omit citations or references; preserve all source attributions.

        Your edits should make the text easier to read, without losing nuance or correctness.
        """

        expected_output = """
        Your output should be a clean, well-structured Markdown document that:

        - Improves clarity, coherence, and grammar
        - Maintains all original facts and intentions
        - Uses professional tone and logical structure
        - Applies proper Markdown formatting (headings, lists, etc.)
        - Preserves all citations and references
        - Is suitable for inclusion in a final report or publication
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
