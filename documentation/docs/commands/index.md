# Gizmo Command Reference

Gizmo provides a streamlined command-line interface with two primary commands that work together to create a powerful research workflow. This reference guide explains each command, its options, and how to use them effectively.

## Available Commands

Gizmo's functionality is organized into two main commands:

1. [`plan`](plan.md) - Creates a structured research plan from your question or topic
2. [`research`](research.md) - Executes the research based on the generated plan

## Command Workflow

Gizmo is designed to work in a simple two-step process:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Your Research  │     │  AI-Generated   │     │  Web Research   │
│    Question     │ ──► │  Research Plan  │ ──► │  & Analysis     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Final Summary  │ ◄── │  Step-by-Step   │ ◄── │  Information    │
│    Report       │     │    Reports      │     │  Organization   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Step 1: Plan Your Research

First, use the [`plan`](plan.md) command to create a structured research plan:

```bash
gizmo plan -p "Your research question here" -o research_plan.md
```

This generates a detailed plan that breaks down your research topic into manageable steps.

### Step 2: Execute the Research

Next, use the [`research`](research.md) command to execute the research based on your plan:

```bash
gizmo research -p research_plan.md -o results_directory
```

This command searches the internet for information related to each step in your plan, analyzes the findings, and creates well-organized reports.

## Command Quick Reference

| Command | Purpose | Key Options |
|---------|---------|-------------|
| [`plan`](plan.md) | Create a research plan | `-p/--prompt`, `-i/--input`, `-s/--size`, `-o/--output` |
| [`research`](research.md) | Execute the research | `-p/--plan`, `-o/--output`, `-m/--memory` |

For detailed information about each command, including all available options and examples, click on the command name in the table above or use the links at the beginning of this page.
