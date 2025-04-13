"""
Summarizer Agents for Gizmo.

This module defines two summarizer agents:
1. Step Summarizer Agent - Produces a concise summary of each step's findings
2. Final Summarizer Agent - Generates a final summary of the entire research project
"""
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat

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
            The Step Summarizer Agent is a specialized assistant designed to create concise summaries 
            of research content. It extracts the most important information and presents it in a 
            clear, brief format that captures the essence of the original content.
        """

        instructions = """
            You are a summarizer. Your task is to create concise summaries of research content.
            Summarize the following text in a few sentences, capturing the main point and any important findings.
            Be concise and clear, focusing on the key insights and conclusions.
            Your summary should be no more than 3-5 sentences or a short paragraph.
            Ensure that the most important facts and findings are preserved in your summary.
        """

        expected_output = """
            Your output should be a concise summary that:

            - Captures the main point and key findings of the original content
            - Is no more than 3-5 sentences or a short paragraph
            - Preserves the most important facts and information
            - Is clear, focused, and easy to understand
            - Maintains the factual accuracy of the original content
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
            The Final Summarizer Agent is a specialized synthesis assistant designed to create 
            comprehensive summaries of entire research projects. It integrates information from 
            multiple research steps to provide a cohesive overview of the findings and insights.
        """

        instructions = """
            You are a research synthesizer. Your task is to create a comprehensive summary of an entire research project.
            Given the summaries of each step of the research, produce an overall summary of the findings.
            This summary should address the original query broadly and highlight key insights from each part of the research.
            Structure your summary with an introduction, key findings section, and conclusion.
            You may use bullet points for separate themes if necessary.
            Keep it concise but comprehensive, focusing on the most significant insights and their implications.
            Your summary should provide a complete picture of what was learned through the research.
        """

        expected_output = """
            Your output should be a well-structured research summary that:

            - Addresses the original research question comprehensively
            - Highlights key insights from each part of the research
            - Has a clear introduction, key findings section, and conclusion
            - Uses bullet points for separate themes where appropriate
            - Is concise but comprehensive
            - Focuses on significant insights and their implications
            - Provides a complete picture of what was learned
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
        str: The summary

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
