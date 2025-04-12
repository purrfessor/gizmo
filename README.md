# G.I.Z.M.O. - AI-Powered Research Assistant

G.I.Z.M.O. is a command-line research assistant that performs in-depth internet research on any topic you're curious about - from academic subjects to everyday questions.

## What Can G.I.Z.M.O. Do For You?

G.I.Z.M.O. helps you research any topic thoroughly without spending hours searching the web yourself. Simply provide a question or topic, and G.I.Z.M.O. will:

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

2. Create the venv and install the package:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -e .
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

## Usage

Using G.I.Z.M.O. is a simple two-step process:

### Step 1: Generate a Research Plan

First, you'll need to create a research plan by providing your question or topic:

```bash
gizmo plan [-i <input_file> | -p <prompt>] [-s <step_number>] [-o <output_file>]
```

Options explained:
- `-i, --input`: Path to a text file containing your research question
- `-p, --prompt`: Type your research question directly in the command
- `-s, --stepnumber`: How many steps you want in your research plan (max: 30)
- `-o, --output`: Where to save your research plan

Note: You must provide either `-i` or `-p` to specify your research question.

Examples:
```bash
# If you have your question in a file:
gizmo plan -i my_question.txt -o research_plan.md

# If you want to type your question directly:
gizmo plan -p "What are the environmental and economic impacts of vertical farming?" -o research_plan.md

# If you want to specify the number of research steps:
gizmo plan -p "How do different dog breeds compare as family pets?" -s 5 -o dog_research_plan.md

# Create a plan with default output location (creates plan.md in current directory):
gizmo plan -p "What are the best practices for container gardening?"

# Create a plan with 10 research steps:
gizmo plan -p "What are the most effective study techniques for college students?" -s 10 -o study_plan.md

# Create a plan from a question file and save to a specific directory:
gizmo plan -i travel_question.txt -o travel_research/plan.md
```

### Viewing and Editing Your Research Plan

After creating your plan, you might want to review or modify it:

```bash
# View your research plan:
cat research_plan.md

# Edit your plan if needed (using your preferred text editor):
nano research_plan.md  # or vim, emacs, etc.

# Count the number of research steps in your plan:
grep -c "^[0-9]" research_plan.md
```

### Step 2: Execute the Research

Once you have a research plan, you can start the research process:

```bash
gizmo research -p <plan_file> -o <output_dir> -m <memory_dir>
```

Options explained:
- `-p, --plan`: Your research plan file from Step 1
- `-o, --output`: Folder where your final research documents will be saved (default: `output`)
- `-m, --memory`: Folder for temporary files created during research (default: `.memory`)

Examples:
```bash
# Basic research execution:
gizmo research -p research_plan.md -o my_research_results

# Specifying a custom memory directory:
gizmo research -p farming_plan.md -o farming_research -m farming_memory

# Running research with default output directory (creates 'output' folder):
gizmo research -p dog_research_plan.md

# Running research and specifying both output and memory directories:
gizmo research -p space_plan.md -o space_research -m space_memory
```

### Working with Output Files

After running your research, you can view the results:

```bash
# List all files in your output directory:
ls my_research_results

# View your final summary:
cat my_research_results/summary_final.md

# View a specific research step:
cat my_research_results/step1.md

# Open all research files in your default text editor (example for macOS):
open my_research_results/*.md

# Count how many research steps were completed:
ls my_research_results/step*.md | wc -l
```

## Output Files

G.I.Z.M.O. creates several types of files during the research process:

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

G.I.Z.M.O. works by breaking down your research question into manageable steps, then researching each step thoroughly:

1. First, it analyzes your question and creates a structured research plan
2. Then it searches for information about each part of your plan
3. Finally, it organizes everything into well-written reports and a comprehensive summary

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

3. G.I.Z.M.O. will approach even this unusual topic systematically, researching:
   - Different hamster breeds and their characteristics
   - Natural behaviors of hamsters that might be useful for alerting
   - Comparison of hamster breeds for trainability
   - Expert opinions on using hamsters as alert animals
   - Alternative pets that might be better suited for the task

## Example Directory

The repository includes an `example/` directory containing a complete research project about "Choosing the best breed of hamsters to use as a guard dog." You can explore these files to see exactly what G.I.Z.M.O. produces:

- `example_prompt.txt`: The original research question
- `plan.md` and `plan.json`: The research plan in different formats
- `step1.md` through `step7.md`: Individual research reports for each step
- `summary_final.md`: The comprehensive final summary

This example demonstrates how G.I.Z.M.O. approaches even unusual research topics in a thorough, structured way.

## Troubleshooting

If you run into any issues:

- **API Key Problems**: Make sure you've correctly set your OpenAI API key as shown in the installation section
- **"Too Many Requests" Errors**: OpenAI may limit how quickly you can make requests. Try:
  - Using fewer research steps
  - Waiting a few minutes before trying again
  - Breaking your research into smaller projects
- **Disk Space**: For very large research projects, check the size of the `.memory` directory and delete it if needed after your research is complete

## Getting Help

If you're having trouble or have questions about using G.I.Z.M.O.:
- Check the example directory to see how a complete research project looks
- Try running a simple research question first to get familiar with the tool
- Refer to this README for command options and examples

## License

This project is licensed under the MIT License - see the LICENSE file for details.
