"""
Research Toolkit for Gizmo.

This module provides a toolkit for reading files in the research output directory.
It allows the researcher agent to access previous research results and the plan.
"""

import os
import re
from typing import List, Dict, Optional

from agno.tools.toolkit import Toolkit
from gizmo.utils.file_utils import read_file


class ResearchToolkit(Toolkit):
    """Toolkit for reading files in the research output directory."""

    def __init__(self, output_dir: str, memory_dir: str, plan_path: Optional[str] = None):
        """
        Initialize the Research Toolkit.

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
        if not self.plan_path or not os.path.exists(self.plan_path):
            return "No plan available."
        
        return read_file(self.plan_path)

    def get_previous_step_result(self, step_number: int) -> str:
        """
        Get the result of a previous research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The result of the step
        """
        if step_number < 1:
            return "Invalid step number."
        
        step_file = os.path.join(self.output_dir, f"step{step_number}.md")
        if not os.path.exists(step_file):
            return f"No result available for step {step_number}."
        
        return read_file(step_file)

    def get_step_analysis(self, step_number: int) -> str:
        """
        Get the analysis of a research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The analysis of the step
        """
        if step_number < 1:
            return "Invalid step number."
        
        analysis_file = os.path.join(self.memory_dir, f"step{step_number}_analysis.md")
        if not os.path.exists(analysis_file):
            return f"No analysis available for step {step_number}."
        
        return read_file(analysis_file)

    def get_step_summary(self, step_number: int) -> str:
        """
        Get the summary of a research step.

        Args:
            step_number (int): The step number

        Returns:
            str: The summary of the step
        """
        if step_number < 1:
            return "Invalid step number."
        
        summary_file = os.path.join(self.memory_dir, f"step{step_number}_summary.md")
        if not os.path.exists(summary_file):
            return f"No summary available for step {step_number}."
        
        return read_file(summary_file)

    def find_relevant_steps(self, query: str, max_steps: int = 3) -> List[Dict[str, str]]:
        """
        Find steps relevant to a query.

        Args:
            query (str): The query to search for
            max_steps (int, optional): Maximum number of steps to return. Defaults to 3.

        Returns:
            List[Dict[str, str]]: List of relevant steps with their content
        """
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
        
        return relevant_steps