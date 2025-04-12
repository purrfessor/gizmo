#!/usr/bin/env python3
"""
Test script for Gizmo CLI with API key.
"""

import subprocess
import sys

def main():
    # The OpenAI API key from the issue description
    api_key = "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"

    # Test the plan command
    print("Testing 'gizmo plan' command with API key...")
    try:
        result = subprocess.run(
            [
                "python3", "-m", "gizmo.cli", 
                "plan", 
                "-i", "example_prompt.txt", 
                "-o", "test_plan.md",
                "-k", api_key
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("Success! Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running command:")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
