# Getting Started with Gizmo

This guide will help you install Gizmo and run your first research project. Follow these simple steps to start using Gizmo as your AI-powered research assistant.

## Prerequisites

Before installing Gizmo, make sure you have:

- **Python 3.8 or higher** installed on your system
- **OpenAI API key** (No ChatGPT subscription needed - you can pay as you go with just an API key)

You can obtain an OpenAI API key from the [OpenAI platform](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key).

## Installation

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

   # For Windows
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e .
   ```

3. Set your OpenAI API key:
   ```bash
   # For macOS/Linux
   export OPENAI_API_KEY='your-api-key'

   # For Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key

   # For Windows (PowerShell)
   $env:OPENAI_API_KEY='your-api-key'
   ```

> 💡 **Tip**: For persistent configuration, consider adding your API key to your environment variables or creating a `.env` file in the project root.

## Your First Research Project

Using Gizmo is a simple two-step process:

### Step 1: Generate a Research Plan

First, create a research plan by providing your question or topic:

```bash
gizmo plan -p "What are the environmental impacts of vertical farming?" -o research_plan.md
```

This command tells Gizmo to:
- Create a research plan (`plan`)
- Use the prompt provided after `-p`
- Save the plan to `research_plan.md`

You can also provide your research question in a text file:

```bash
gizmo plan -i my_question.txt -o research_plan.md
```

#### Customize Your Research Plan Size

For more complex topics, you can specify the size of your research plan:

```bash
# For a medium-sized research plan (10-30 steps)
gizmo plan -p "How do different dog breeds compare as family pets?" -s medium -o dog_plan.md

# For a large, comprehensive research plan (30-70 steps)
gizmo plan -p "What are effective study techniques for college students?" -s large -o study_plan.md
```

### Step 2: Execute the Research

Once you have a research plan, start the research process:

```bash
gizmo research -p research_plan.md -o my_research_results
```

This command tells Gizmo to:
- Execute the research based on your plan (`research`)
- Use the plan file specified after `-p`
- Save the results to the directory specified after `-o`

## Understanding Your Results

After running your research, Gizmo creates several files in your output directory:

- `plan.md`: Your research plan showing all the steps
- `step1.md`, `step2.md`, etc.: Well-written reports for each research step
- `summary_final.md`: Comprehensive summary of all findings

To view your results:

```bash
# View your final summary:
cat my_research_results/summary_final.md

# View a specific research step:
cat my_research_results/step1.md
```

## Example: Researching Vertical Farming

Let's walk through a complete example:

1. Create a research plan:
   ```bash
   gizmo plan -p "What are the environmental and economic impacts of vertical farming?" -o farming_plan.md
   ```

2. Execute the research:
   ```bash
   gizmo research -p farming_plan.md -o farming_results
   ```

3. Review your results in the `farming_results` directory:
   - `step1.md`, `step2.md`, etc.: Detailed reports on each aspect
   - `summary_final.md`: Overall summary of findings

## Next Steps

Now that you've run your first research project with Gizmo, you can:

- Explore more [use cases](use-cases/index.md) for Gizmo
- Learn about advanced [command options](commands/index.md)
- Try the deep research mode for more comprehensive results

Happy researching with Gizmo!
