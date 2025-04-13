"""
Summarizer Agents for Gizmo.

This module defines two summarizer agents:
1. Step Summarizer Agent - Produces a concise summary of each step's findings
2. Final Summarizer Agent - Generates a final summary of the entire research project
"""
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.response import RunResponse

from gizmo.utils.error_utils import retry, handle_agent_error
from gizmo.utils.file_utils import write_file


class StepSummarizerAgent(Agent):
    def __init__(self):
        """
        Create and configure the Step Summarizer Agent.

        Returns:
            Agent: The configured step summarizer agent
        """

        description = """
        The Step Summarizer Agent is a focused assistant that distills individual research step findings into clear, concise summaries. 
        It interacts with detailed content and extracts the most relevant points, presenting them in a brief format that is easy to digest. 
        The agent maintains accuracy while reducing verbosity, offering quick overviews of what was learned at each stage.
        """

        instructions = """
        You are a summarization agent assigned to distill research findings into brief, accurate summaries.

        1. Read the provided research content carefully.
        2. Identify the key ideas, conclusions, or findings.
        3. Write a concise summary (3-10 sentences) that captures the essence of the content.
        4. Avoid unnecessary detail and focus on what's most important.
        5. Maintain the factual accuracy and tone of the original content.

        Keep your summary tight, informative, and suitable for quick review.
        """

        expected_output = """
        Your output should be a brief, clear summary that:

        - Captures the most important points of the original research step
        - Is no longer than 3–10 sentences or a short paragraph
        - Maintains factual accuracy and avoids unnecessary detail
        - Is easy to understand and suitable for quick reading
        """

        super().__init__(
            name="Step Summarizer",
            role="Summarizer",
            model=OpenAIChat(id="gpt-3.5-turbo"),  # efficient for summarization
            tools=[],  # no external tools needed
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )


class FinalSummarizerAgent(Agent):
    def __init__(self):
        """
        Create and configure the Final Summarizer Agent.

        Returns:
            Agent: The configured final summarizer agent
        """

        description = """
        The Final Summarizer Agent synthesizes findings from multiple research steps to produce a coherent and insightful final summary. 
        It captures the overarching themes, highlights key discoveries, and presents them in a structured and digestible format. 
        The tone is comprehensive yet accessible, aiming to convey the complete research narrative.
        """

        instructions = """
        You are a final summarization agent tasked with synthesizing the results of a complete research process.

        1. Review all the step summaries provided.
        2. Extract recurring themes, major insights, and key takeaways.
        3. Structure your summary into three parts: introduction, key findings, and conclusion.
        4. Use bullet points in the key findings section where helpful.
        5. Keep your summary clear and logically organized, with emphasis on clarity and cohesion.

        Your goal is to convey a full picture of the research in a single, polished narrative.
        """

        expected_output = """
        Your output should be a well-structured research summary that:

        - Includes an introduction, key findings section, and conclusion
        - Integrates insights from all steps of the research
        - Uses bullet points for clarity where appropriate
        - Stays focused, cohesive, and informative
        - Communicates the core takeaways in an accessible manner
        """

        super().__init__(
            name="Final Summarizer",
            role="Synthesizer",
            model=OpenAIChat(id="gpt-4o"),  # better for synthesis across multiple topics
            tools=[],  # no external tools needed
            description=description,
            instructions=instructions,
            expected_output=expected_output,
            markdown=True
        )


@retry(max_attempts=2, delay=1.0)
def run_step_summarizer_agent(polished_report, step_number, memory_dir):
    """
    Run the Step Summarizer Agent for a step.

    Args:
        polished_report (str): The polished report from the writer
        step_number (int): The step number
        memory_dir (str): Directory to save intermediate files

    Returns:
        RunResponse: The summary

    Raises:
        Exception: If the step summarizer agent fails after retries
    """
    try:
        # Create the step summarizer agent
        summarizer = StepSummarizerAgent()
        from gizmo.utils.error_utils import logger

        # Run the step summarizer agent
        response = summarizer.run(polished_report)

        # Save the summary
        summary_file = os.path.join(memory_dir, f"step{step_number}_summary.md")
        write_file(summary_file, response.content)

        return response
    except Exception as e:
        # Generate a simple summary as fallback
        fallback = f"This step covered: {polished_report[:100]}..."
        write_file(os.path.join(memory_dir, f"step{step_number}_summary.md"), fallback)
        return handle_agent_error("Step Summarizer", step_number, e, fallback)


@retry(max_attempts=2, delay=1.0)
def run_final_summarizer_agent(step_summaries, output_dir):
    """
    Run the Final Summarizer Agent.

    Args:
        step_summaries (list): List of step summaries
        output_dir (str): Directory to save output files

    Returns:
        str: The final summary

    Raises:
        Exception: If the final summarizer agent fails after retries
    """
    try:
        # Create the final summarizer agent
        summarizer = FinalSummarizerAgent()
        from gizmo.utils.error_utils import logger

        # Prepare the input for the final summarizer
        summarizer_input = "# Research Step Summaries\n\n" + "\n\n".join(step_summaries)

        # Run the final summarizer agent
        response = summarizer.run(summarizer_input)

        # Save the final summary
        summary_file = os.path.join(output_dir, "summary_final.md")
        write_file(summary_file, response.content)

        return response
    except Exception as e:
        # Generate a simple summary as fallback
        fallback = "# Research Summary\n\n" + "\n\n".join(step_summaries)
        write_file(os.path.join(output_dir, "summary_final.md"), fallback)
        return handle_agent_error("Final Summarizer", 0, e, fallback)
