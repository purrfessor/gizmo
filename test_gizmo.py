#!/usr/bin/env python3
"""
Test script for Gizmo.

This script tests the basic functionality of the Gizmo tool by running a simple
plan and research workflow.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def run_command(command):
    """Run a command and return its output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout


def main():
    """Run the test."""
    # Create temporary directories
    temp_dir = tempfile.mkdtemp()
    output_dir = os.path.join(temp_dir, "output")
    memory_dir = os.path.join(temp_dir, "memory")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(memory_dir, exist_ok=True)

    try:
        # Check if example_prompt.txt exists
        if not os.path.exists("example_prompt.txt"):
            print("Error: example_prompt.txt not found")
            sys.exit(1)

        # Test the plan command
        plan_file = os.path.join(temp_dir, "plan.md")
        run_command([
            "./gizmo.py", "plan",
            "-i", "example_prompt.txt",
            "-o", plan_file
        ])

        # Check if the plan file was created
        if not os.path.exists(plan_file):
            print("Error: Plan file was not created")
            sys.exit(1)

        print(f"Plan file created: {plan_file}")
        with open(plan_file, "r") as f:
            plan_content = f.read()
            print("\nPlan content:")
            print("=" * 40)
            print(plan_content[:500] + "..." if len(plan_content) > 500 else plan_content)
            print("=" * 40)

        # Test the research command with a limited number of steps
        # Note: For testing purposes, we'll modify the plan to include only the first step
        # This is to make the test run faster
        with open(plan_file, "r") as f:
            plan_lines = f.readlines()
        
        # Keep only the first step
        with open(plan_file, "w") as f:
            # Write the header and the first step
            for i, line in enumerate(plan_lines):
                f.write(line)
                if i > 5 and line.strip().startswith("1."):
                    break

        # Run the research command
        run_command([
            "./gizmo.py", "research",
            "-p", plan_file,
            "-o", output_dir,
            "-m", memory_dir
        ])

        # Check if the output files were created
        step1_file = os.path.join(output_dir, "step1.md")
        summary_file = os.path.join(output_dir, "summary_final.md")

        if not os.path.exists(step1_file):
            print("Error: Step 1 file was not created")
            sys.exit(1)

        if not os.path.exists(summary_file):
            print("Error: Summary file was not created")
            sys.exit(1)

        print(f"Step 1 file created: {step1_file}")
        print(f"Summary file created: {summary_file}")

        # Print the summary content
        with open(summary_file, "r") as f:
            summary_content = f.read()
            print("\nSummary content:")
            print("=" * 40)
            print(summary_content[:500] + "..." if len(summary_content) > 500 else summary_content)
            print("=" * 40)

        print("\nTest completed successfully!")

    finally:
        # Clean up
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()