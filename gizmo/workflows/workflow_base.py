"""
Base workflow for Gizmo.

This module defines the abstract base class for all Gizmo workflows.
"""

from abc import ABC, abstractmethod


class GizmoWorkflow(ABC):
    """
    Base class for Gizmo workflows.

    This abstract class defines the interface for all Gizmo workflows.
    Concrete implementations should override the run_plan and run_research methods.
    """

    @abstractmethod
    def run_plan(self, input_prompt, output_plan_path, is_file=True, size=None):
        """
        Generate a research plan from a prompt.

        Args:
            input_prompt (str): Path to the input prompt file or the prompt text itself
            output_plan_path (str): Path to save the output plan
            is_file (bool, optional): Whether input_prompt is a file path. Defaults to True.
            size (str, optional): Size of the research plan ("small", "medium", "large"). Defaults to None.

        Returns:
            str: The generated plan

        Raises:
            Exception: If the plan generation fails after retries
        """
        pass

    @abstractmethod
    async def run_research(self, plan_path, output_dir, memory_dir=".memory", deep=False, initial_input=None):
        """
        Execute a research workflow based on a plan.

        Args:
            plan_path (str): Path to the plan file
            output_dir (str): Directory to save the output files
            memory_dir (str): Directory to save intermediate files
            deep (bool): Whether to use GPT Researcher for deep research
            initial_input (str, optional): Initial input for the research

        Raises:
            Exception: If the research execution fails
        """
        pass