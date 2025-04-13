"""
Workflow orchestration for Gizmo.

This module provides standalone functions for the Gizmo CLI to:
1. Generate a research plan from a prompt
2. Execute a research workflow based on a plan

These functions are wrappers around the workflow implementations in workflow_basic.py and workflow_deep.py.
"""

import os

from gizmo.workflows.workflow_basic import basic_workflow
from gizmo.workflows.workflow_deep import deep_workflow


def run_plan(input_prompt, output_plan_path, is_file=True, size=None):
    """
    Generate a research plan from a prompt.

    This is a standalone function for backward compatibility.
    It creates a BasicGizmoWorkflow instance and calls its run_plan method.

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
    return basic_workflow.run_plan(input_prompt, output_plan_path, is_file, size)


async def run_research(plan_path, output_dir, memory_dir=".memory", deep=False, initial_input=None):
    """
    Execute a research workflow based on a plan.

    This is a standalone function for backward compatibility.
    It creates the appropriate workflow instance based on the deep parameter and calls its run_research method.

    Args:
        plan_path (str): Path to the plan file
        output_dir (str): Directory to save the output files
        memory_dir (str): Directory to save intermediate files
        deep (bool): Whether to use GPT Researcher for deep research
        initial_input (str, optional): Initial input for the research

    Raises:
        Exception: If the research execution fails
    """
    # Set default retriever to duckduckgo if not already set
    if "RETRIEVER" not in os.environ:
        os.environ["RETRIEVER"] = "duckduckgo"

    # Use the appropriate workflow based on the deep parameter
    if deep:
        return await deep_workflow.run_research(plan_path, output_dir, memory_dir, deep, initial_input)
    else:
        return await basic_workflow.run_research(plan_path, output_dir, memory_dir, deep, initial_input)
