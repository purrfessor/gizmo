"""
Research Context Toolkit for Gizmo.

This module provides a toolkit for reading files in the research output directory.
It allows the researcher agent to access previous research results and the plan.
"""

import os
import re
import time
from typing import List, Dict, Optional

from agno.tools.toolkit import Toolkit
from gizmo.utils.error_utils import logger
from gizmo.utils.file_utils import read_file


class ResearchContextToolkit(Toolkit):
    """Toolkit for reading files in the research output directory."""

    def __init__(self, output_dir: str, memory_dir: str, plan_path: Optional[str] = None):
        """
        Initialize the ResearchContextToolkit.

        Args:
            output_dir (str): Directory containing the output files
            memory_dir (str): Directory containing the memory files
            plan_path (Optional[str]): Path to the plan file
        """
        self.output_dir = output_dir
        self.memory_dir = memory_dir
        self.plan_path = plan_path
        super().__init__()

    @property
    def instructions(self) -> str:
        """Return instructions for using the toolkit."""
        return (
            "This toolkit allows you to read files from the research output directory. "
            "You can use it to access previous research results and the plan."
        )

    def get_plan(self) -> str:
        """
        Get the research plan.

        Returns:
            str: The research plan
        """
        start_time = time.time()
        logger.info(f"ResearchContextToolkit: Calling get_plan()")

        if not self.plan_path or not os.path.exists(self.plan_path):
            logger.info(f"ResearchContextToolkit: No plan available")
            return "No plan available."

        result = read_file(self.plan_path)
        elapsed_time = time.time() - start_time
        logger.info(f"ResearchContextToolkit: get_plan() completed in {elapsed_time:.2f}s")
        return result

    def get_previous_step_result(self, step_number: int) -> str:
        """
        Get the result of a previous research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The result of the step
        """
        start_time = time.time()
        logger.info(f"ResearchContextToolkit: Calling get_previous_step_result(step_number={step_number})")

        if step_number < 1:
            logger.info(f"ResearchContextToolkit: Invalid step number: {step_number}")
            return "Invalid step number."

        step_file = os.path.join(self.output_dir, f"step{step_number}.md")
        if not os.path.exists(step_file):
            logger.info(f"ResearchContextToolkit: No result available for step {step_number}")
            return f"No result available for step {step_number}."

        result = read_file(step_file)
        elapsed_time = time.time() - start_time
        logger.info(f"ResearchContextToolkit: get_previous_step_result() completed in {elapsed_time:.2f}s")
        return result

    def get_step_analysis(self, step_number: int) -> str:
        """
        Get the analysis of a research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The analysis of the step
        """
        start_time = time.time()
        logger.info(f"ResearchContextToolkit: Calling get_step_analysis(step_number={step_number})")

        if step_number < 1:
            logger.info(f"ResearchContextToolkit: Invalid step number: {step_number}")
            return "Invalid step number."

        analysis_file = os.path.join(self.memory_dir, f"step{step_number}_analysis.md")
        if not os.path.exists(analysis_file):
            logger.info(f"ResearchContextToolkit: No analysis available for step {step_number}")
            return f"No analysis available for step {step_number}."

        result = read_file(analysis_file)
        elapsed_time = time.time() - start_time
        logger.info(f"ResearchContextToolkit: get_step_analysis() completed in {elapsed_time:.2f}s")
        return result

    def get_step_summary(self, step_number: int) -> str:
        """
        Get the summary of a research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The summary of the step
        """
        start_time = time.time()
        logger.info(f"ResearchContextToolkit: Calling get_step_summary(step_number={step_number})")

        if step_number < 1:
            logger.info(f"ResearchContextToolkit: Invalid step number: {step_number}")
            return "Invalid step number."

        summary_file = os.path.join(self.memory_dir, f"step{step_number}_summary.md")
        if not os.path.exists(summary_file):
            logger.info(f"ResearchContextToolkit: No summary available for step {step_number}")
            return f"No summary available for step {step_number}."

        result = read_file(summary_file)
        elapsed_time = time.time() - start_time
        logger.info(f"ResearchContextToolkit: get_step_summary() completed in {elapsed_time:.2f}s")
        return result

    def find_relevant_steps(self, query: str, max_steps: int = 3) -> List[Dict[str, str]]:
        """
        Find steps relevant to a query.

        Args:
            query (str): The query to search for
            max_steps (int, optional): Maximum number of steps to return. Defaults to 3.

        Returns:
            List[Dict[str, str]]: List of relevant steps with their content
        """
        start_time = time.time()
        logger.info(f"ResearchContextToolkit: Calling find_relevant_steps(query='{query}', max_steps={max_steps})")

        # Get all step files
        step_files = []
        for filename in os.listdir(self.output_dir):
            if re.match(r"step\d+\.md", filename):
                step_number = int(re.search(r"step(\d+)\.md", filename).group(1))
                step_files.append((step_number, os.path.join(self.output_dir, filename)))

        # Sort by step number
        step_files.sort()

        # Find relevant steps
        relevant_steps = []
        for step_number, file_path in step_files:
            content = read_file(file_path)
            # Simple relevance check: if query terms appear in the content
            if query.lower() in content.lower():
                relevant_steps.append({
                    "step_number": step_number,
                    "content": content
                })
                if len(relevant_steps) >= max_steps:
                    break

        elapsed_time = time.time() - start_time
        logger.info(f"ResearchContextToolkit: find_relevant_steps() found {len(relevant_steps)} relevant steps in {elapsed_time:.2f}s")
        return relevant_steps
