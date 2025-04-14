# G.I.Z.M.O. - AI-Powered Research Assistant

![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Documentation](https://img.shields.io/badge/docs-website-orange)](https://purrfessor.github.io/gizmo/)

`gizmo` is a command-line research assistant that performs in-depth internet research on any topic you're curious about - from academic subjects to everyday questions.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Output Files](#output-files)
6. [How It Works](#how-it-works)
7. [Example Research Projects](#example-research-projects)
8. [Troubleshooting](#troubleshooting)
9. [Getting Help](#getting-help)
10. [Documentation](#documentation)
11. [License](#license)

## Introduction

`gizmo` helps you research any topic thoroughly without spending hours searching the web yourself. Simply provide a question or topic, and `gizmo` will:

1. Break down your topic into manageable research steps
2. Search the internet for relevant information
3. Analyze and organize the findings
4. Create well-written reports for each aspect of your research
5. Provide a comprehensive summary of everything it discovered

## Features

- **Simple Two-Step Process**: First plan your research, then execute it with a single command
- **Comprehensive Research**: Automatically searches multiple sources for thorough information
- **Easy-to-Read Results**: All research saved as Markdown files you can view in any text editor
- **Reliable Performance**: Built-in mechanisms to handle connection issues or timeouts
- **Flexible Usage**: Works with a wide range of research topics and questions
- **AI-Powered Analysis**: Utilizes advanced AI to process and synthesize information

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (No ChatGPT subscription needed - you can pay as you go with just an API key from the [OpenAI platform](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key))

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gizmo.git
   cd gizmo
   ```

2. Create a virtual environment and install the package:
   ```bash
   # For macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -e .
   ```
   
   ```bash
   # For Windows
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e .
   ```

3. Set your OpenAI API key:
   ```bash
   # For macOS/Linux
   export OPENAI_API_KEY='your-api-key'
   ```
   
   ```bash
   # For Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key
   ```

   ```bash
   # For Windows (PowerShell)
   $env:OPENAI_API_KEY='your-api-key'
   ```

> 💡 **Tip**: For persistent configuration, consider adding your API key to your environment variables or creating a `.env` file in the project root.

## Usage

Using `gizmo` is a simple two-step process:

### Step 1: Generate a Research Plan 📝

First, create a research plan by providing your question or topic:

```bash
gizmo plan [-i <input_file> | -p <prompt>] [-s <size>] [-o <output_file>]
```

#### Options:
| Option | Description |
|--------|-------------|
| `-i, --input` | Path to a text file containing your research question |
| `-p, --prompt` | Type your research question directly in the command |
| `-s, --size` | Size of the research plan: small (1-10 steps), medium (10-30 steps), large (30-70 steps). Default: small |
| `-o, --output` | Where to save your research plan |

> **Note**: You must provide either `-i` or `-p` to specify your research question.

#### Examples:

```bash
# If you have your question in a file:
gizmo plan -i my_question.txt -o research_plan.md

# If you want to type your question directly:
gizmo plan -p "What are the environmental impacts of vertical farming?" -o research_plan.md

# For a medium-sized research plan:
gizmo plan -p "How do different dog breeds compare as family pets?" -s medium -o dog_plan.md

# For a large, comprehensive research plan:
gizmo plan -p "What are effective study techniques for college students?" -s large -o study_plan.md
```

### Viewing and Editing Your Research Plan

After creating your plan, you can review or modify it:

```bash
# View your research plan:
cat research_plan.md

# Edit your plan if needed:
nano research_plan.md  # or use your preferred text editor
```

### Step 2: Execute the Research 🔍

Once you have a research plan, start the research process:

```bash
gizmo research -p <plan_file> -o <output_dir> -m <memory_dir>
```

#### Options:
| Option | Description |
|--------|-------------|
| `-p, --plan` | Your research plan file from Step 1 |
| `-o, --output` | Folder where your final research documents will be saved (default: `output`) |
| `-m, --memory` | Folder for temporary files created during research (default: `.memory`) |

#### Examples:

```bash
# Basic research execution:
gizmo research -p research_plan.md -o my_research_results

# With custom memory directory:
gizmo research -p farming_plan.md -o farming_research -m farming_memory

# Using default output directory:
gizmo research -p dog_research_plan.md
```

### Working with Output Files 📄

After running your research, view the results:

```bash
# View your final summary:
cat my_research_results/summary_final.md

# View a specific research step:
cat my_research_results/step1.md

# Open all research files (macOS example):
open my_research_results/*.md
```

> 💡 **Tip**: The summary_final.md file contains the comprehensive overview of all research findings and is a great place to start reviewing your results.

## Output Files

`gizmo` creates several types of files during the research process:

### File Structure Overview

```
project/
├── .memory/                  # Working files (temporary)
│   ├── stepX_search.md       # Raw information from web searches
│   ├── stepX_analysis.md     # Analysis of collected information
│   └── stepX_summary.md      # Brief summary of findings
│
└── output/                   # Final research results
    ├── plan.md               # Your research plan
    ├── step1.md              # Detailed report for step 1
    ├── step2.md              # Detailed report for step 2
    ├── ...                   # Additional step reports
    └── summary_final.md      # Comprehensive summary of all findings
```

### Memory Files (Working Files)

These are temporary files stored in the `.memory/` folder (or your custom location with `-m`):
- `stepX_search.md`: Information collected from the web for each step
- `stepX_analysis.md`: Detailed analysis of the collected information
- `stepX_summary.md`: Brief summary of what was found in each step

### Output Files (Your Research Results)

These are your final research documents stored in the `output/` folder (or your custom location with `-o`):
- `plan.md`: Your research plan showing all the steps
- `stepX.md`: Well-written report for each research step
- `summary_final.md`: Comprehensive summary of all findings

All files are in Markdown format (.md), which you can open with any text editor or view with a Markdown viewer for better formatting.

## How It Works

`gizmo` works by breaking down your research question into manageable steps, then researching each step thoroughly:

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

1. **Analysis**: It analyzes your question and creates a structured research plan
2. **Research**: It searches for information about each part of your plan
3. **Synthesis**: It organizes everything into well-written reports
4. **Summary**: It creates a comprehensive summary of all findings

## Example Research Projects

### Example 1: Environmental Impact of Vertical Farming

1. Create a file `farming_question.txt` with your research question:
   ```
   What are the environmental and economic impacts of vertical farming?
   ```

2. Generate a research plan:
   ```bash
   gizmo plan -i farming_question.txt -o farming_plan.md
   ```

3. Execute the research:
   ```bash
   gizmo research -p farming_plan.md -o farming_results
   ```

4. Review your results in the `farming_results` directory:
   - `step1.md`, `step2.md`, etc.: Detailed reports on each aspect
   - `summary_final.md`: Overall summary of findings

### Example 2: Hamsters as Guard Animals

1. Create a file with an unusual research question:
   ```
   Choosing the best breed of hamsters to use as a guard dog (hamster).
   ```

2. Generate a research plan and run the research as shown above

3. `gizmo` will approach even this unusual topic systematically, researching:
   - Different hamster breeds and their characteristics
   - Natural behaviors of hamsters that might be useful for alerting
   - Comparison of hamster breeds for trainability
   - Expert opinions on using hamsters as alert animals
   - Alternative pets that might be better suited for the task

## Example Directory

The repository includes an `example/` directory containing a complete research project about "Choosing the best breed of hamsters to use as a guard dog." You can explore these files to see exactly what `gizmo` produces:

- `example_prompt.txt`: The original research question
- `plan.md` and `plan.json`: The research plan in different formats
- `step1.md` through `step7.md`: Individual research reports for each step
- `summary_final.md`: The comprehensive final summary

This example demonstrates how `gizmo` approaches even unusual research topics in a thorough, structured way.

## Troubleshooting

If you run into any issues:

### Common Problems and Solutions

| Problem | Solution |
|---------|----------|
| **API Key Errors** | Ensure your OpenAI API key is correctly set as shown in the installation section |
| **"Too Many Requests"** | OpenAI may limit request frequency. Try using a smaller plan size (`-s small`), waiting a few minutes, or breaking your research into smaller projects |
| **Disk Space Issues** | For large research projects, check the size of the `.memory` directory and delete it if needed after your research is complete |
| **Slow Performance** | Consider using a smaller research plan size or breaking your research into multiple smaller projects |
| **Network Errors** | Check your internet connection and try again. Gizmo has built-in retry mechanisms for temporary network issues |

## Getting Help

If you're having trouble or have questions about using `gizmo`:

- **Examples**: Check the example directory to see how a complete research project looks
- **Start Small**: Try running a simple research question first to get familiar with the tool
- **Documentation**: Refer to this README for command options and examples

## Documentation

For comprehensive documentation on Gizmo, visit our [documentation website](https://purrfessor.github.io/gizmo/).

The documentation includes:
- Detailed installation instructions
- Command reference with all available options
- Use case examples for research and development assistance
- Information on observability and token usage tracking
- Guides for getting the most out of Gizmo

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This README was written by Junie who used the documentation, which was so kindly generated by gizmo, as a guide.
