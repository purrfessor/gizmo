"""
File utilities for Gizmo.

This module provides utility functions for file operations like reading and writing files.
"""

import os
import re
import json
from pathlib import Path


def read_file(file_path):
    """
    Read the content of a file.

    Args:
        file_path (str): Path to the file to read

    Returns:
        str: Content of the file

    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def write_file(file_path, content):
    """
    Write content to a file.

    Args:
        file_path (str): Path to the file to write
        content (str): Content to write to the file

    Raises:
        IOError: If there's an error writing to the file
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {str(e)}")


def ensure_dir(directory):
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory (str): Path to the directory

    Raises:
        IOError: If there's an error creating the directory
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except IOError as e:
        raise IOError(f"Error creating directory {directory}: {str(e)}")


def parse_plan_file(plan_path):
    """
    Parse a plan file to extract the list of steps.

    Args:
        plan_path (str): Path to the plan file

    Returns:
        list: List of steps extracted from the plan

    Raises:
        ValueError: If the plan file doesn't contain a valid list of steps
    """
    # First, check if there's a corresponding JSON file
    json_path = plan_path.replace(".md", ".json")
    if os.path.exists(json_path):
        try:
            # Try to parse the JSON file
            json_content = read_file(json_path)
            plan_data = json.loads(json_content)

            # Extract the topics from the JSON data
            steps = [item.get("topic", "") for item in plan_data if item.get("topic")]

            if steps:
                return steps
        except (json.JSONDecodeError, IOError):
            # If there's an error parsing the JSON, fall back to the Markdown file
            pass

    # If no JSON file or parsing failed, read the Markdown file
    content = read_file(plan_path)

    # Try to parse the content as JSON first
    try:
        plan_data = json.loads(content)
        steps = [item.get("topic", "") for item in plan_data if item.get("topic")]
        if steps:
            return steps
    except json.JSONDecodeError:
        # If JSON parsing fails, fall back to regex-based parsing
        pass

    # Extract numbered list items using regex
    # This pattern matches lines starting with a number followed by a period or parenthesis
    steps = re.findall(r'^\s*\d+[\.\)]\s*(.+)$', content, re.MULTILINE)

    if not steps:
        # Try to match Markdown list items (lines starting with *)
        steps = re.findall(r'^\s*\*\s*(.+)$', content, re.MULTILINE)

    if not steps:
        # Try to match lines with "Step X:" format
        steps = re.findall(r'^\s*Step\s+\d+:?\s*(.+)$', content, re.MULTILINE)

    if not steps:
        raise ValueError(f"Could not extract steps from plan file: {plan_path}")

    return steps


def formulate_search_query(step):
    """
    Formulate a search query from a step description.

    Args:
        step (str): Step description

    Returns:
        str: Search query
    """
    # Remove any formatting or special characters
    query = re.sub(r'[^\w\s]', ' ', step)

    # Remove extra whitespace
    query = ' '.join(query.split())

    return query
