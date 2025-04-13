#!/usr/bin/env python3
"""
Gizmo CLI - A research assistant powered by Agno framework.

This module provides the command-line interface for Gizmo, allowing users to:
1. Generate a research plan from a prompt
2. Execute a research workflow based on a plan

Usage:
    gizmo plan [-i <input_file> | -p <prompt>] [-s <size>] [-o <output_path>]
    gizmo research [-p <plan_file>] [-o <output_dir>] [--deep]

Note: For the plan command, either -i or -p must be provided.
      The -s option allows specifying the size of the research plan: small (1-10 steps), 
      medium (10-30 steps), or large (30-70 steps). Default is small.
      For the -o option, if the path ends with '.md', it writes directly to that file.
      Otherwise, it creates a directory and writes to 'plan.md' inside it.
      For the research command, if -p is not provided, it looks for the plan in './output/plan.md' by default.
      The --deep flag enables deep research using GPT Researcher, which produces more comprehensive
      research for each step instead of using the standard multi-agent approach.
"""

import argparse
import os
import sys
import asyncio

from gizmo.workflows.workflow import run_plan, run_research


def setup_parser():
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Gizmo - A research assistant powered by Agno framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Plan command
    plan_parser = subparsers.add_parser(
        "plan", help="Generate a research plan from a prompt"
    )
    plan_parser.add_argument(
        "-i", "--input", required=False, help="Input file containing the research prompt"
    )
    plan_parser.add_argument(
        "-p", "--prompt", help="Direct research prompt text"
    )
    plan_parser.add_argument(
        "-s", "--size", choices=["small", "medium", "large"], default="small",
        help="Size of the research plan: small (1-10 steps), medium (10-30 steps), large (30-70 steps). Default: small"
    )
    plan_parser.add_argument(
        "-o", "--output", default="output/plan.md",
        help="Output path for the research plan. If it ends with '.md', writes directly to that file. "
             "Otherwise, creates a directory and writes to 'plan.md' inside it. (default: output/plan.md)"
    )
    plan_parser.add_argument(
        "-k", "--api-key", help="OpenAI API key (overrides OPENAI_API_KEY environment variable)"
    )

    # Research command
    research_parser = subparsers.add_parser(
        "research", help="Execute a research workflow based on a plan"
    )
    research_parser.add_argument(
        "-p", "--plan", default="./output/plan.md", help="Input file containing the research plan (default: ./output/plan.md)"
    )
    research_parser.add_argument(
        "-o", "--output", default="output", help="Output directory for research results (default: output)"
    )
    research_parser.add_argument(
        "-m", "--memory", default=".memory", help="Directory for intermediate files (default: .memory)"
    )
    research_parser.add_argument(
        "-k", "--api-key", help="OpenAI API key (overrides OPENAI_API_KEY environment variable)"
    )
    research_parser.add_argument(
        "--deep", action="store_true", help="Use GPT Researcher for deep research"
    )
    research_parser.add_argument(
        "--initial-input", help="Path to a file containing initial input for the research"
    )

    return parser


def main():
    """Main entry point for the Gizmo CLI."""
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check if OpenAI API key is provided as argument or set as environment variable
    if hasattr(args, 'api_key') and args.api_key:
        # Use the API key provided as a command-line argument
        os.environ["OPENAI_API_KEY"] = args.api_key
    elif not os.environ.get("OPENAI_API_KEY"):
        print("Error: OpenAI API key not provided.")
        print("Please either:")
        print("  - Use the -k/--api-key option: gizmo {} -k 'your-api-key' ...".format(args.command))
        print("  - Set the OPENAI_API_KEY environment variable: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    try:
        if args.command == "plan":
            # Validate that either input file or prompt is provided
            if not args.input and not args.prompt:
                print("Error: Either -i/--input or -p/--prompt must be provided.")
                print("Use -i/--input to specify an input file or -p/--prompt to provide the prompt directly.")
                sys.exit(1)

            # If input file is provided, validate it exists
            if args.input and not os.path.exists(args.input):
                print(f"Error: Input file '{args.input}' does not exist.")
                sys.exit(1)

            # Process output parameter
            if args.output.endswith(".md"):
                # If output ends with .md, use it directly as the output file path
                output_path = args.output
                # Create output directory if it doesn't exist
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            else:
                # If output doesn't end with .md, use it as a directory and put plan.md inside
                output_dir = args.output
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_path = os.path.join(output_dir, "plan.md")

            if args.input:
                print(f"Generating research plan from file '{args.input}'...")
                run_plan(args.input, output_path, size=args.size)
            else:
                print("Generating research plan from provided prompt...")
                run_plan(args.prompt, output_path, is_file=False, size=args.size)

            print(f"Research plan saved to '{output_path}'")

        elif args.command == "research":
            # Validate plan file exists
            if not os.path.exists(args.plan):
                print(f"Error: Plan file '{args.plan}' does not exist.")
                sys.exit(1)

            # Create output directory if it doesn't exist
            if not os.path.exists(args.output):
                os.makedirs(args.output)

            # Create memory directory if it doesn't exist
            if not os.path.exists(args.memory):
                os.makedirs(args.memory)

            # Read initial input file if provided
            initial_input = None
            if args.initial_input:
                if not os.path.exists(args.initial_input):
                    print(f"Error: Initial input file '{args.initial_input}' does not exist.")
                    sys.exit(1)
                with open(args.initial_input, 'r', encoding='utf-8') as f:
                    initial_input = f.read()
                print(f"Using initial input from '{args.initial_input}'")

            print(f"Executing research based on plan '{args.plan}'...")
            asyncio.run(run_research(args.plan, args.output, args.memory, args.deep, initial_input))
            print(f"Research completed. Results saved to '{args.output}'")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
