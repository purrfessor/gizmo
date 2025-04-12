# G.I.Z.M.O. - AI-Powered Research Assistant

G.I.Z.M.O. is a command-line research assistant powered by the Agno framework and OpenAI models. It orchestrates multiple specialized AI agents to perform in-depth internet research on any topic.

## Features

- **Multi-Agent Architecture**: Specialized agents for planning, web searching, analysis, writing, and summarization
- **Two-Phase Research Process**: Planning phase to break down complex topics, followed by a research phase to investigate each aspect
- **Transparent Outputs**: All results saved as Markdown files for easy reading and sharing
- **Error Resilience**: Built-in retry mechanisms and fallbacks to handle API errors or timeouts
- **Modular Design**: Easy to extend with new agent types or capabilities

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gizmo.git
   cd gizmo
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

## Usage

Gizmo offers two main commands:

### 1. Generate a Research Plan

```bash
gizmo plan [-i <input_file> | -p <prompt>] [-o <output_file>]
```

- `-i, --input`: Path to a text file containing your research prompt
- `-p, --prompt`: Direct research prompt text
- `-o, --output`: Path where the research plan will be saved (default: `plan.md`)

Note: Either `-i` or `-p` must be provided.

Examples:
```bash
# Using an input file
gizmo plan -i my_question.txt -o research_plan.md

# Using a direct prompt
gizmo plan -p "What are the environmental and economic impacts of vertical farming?" -o research_plan.md
```

### 2. Execute Research Based on a Plan

```bash
gizmo research -p <plan_file> -o <output_dir> -m <memory_dir>
```

- `-p, --plan`: Path to the research plan file
- `-o, --output`: Directory where final research documents will be saved (default: `output`)
- `-m, --memory`: Directory for intermediate files (default: `.memory`)

Example:
```bash
gizmo research -p research_plan.md -o my_research_results
```

## Output Files

Gizmo produces several types of files during execution:

### Memory Files (Intermediate Data)

Stored in the `.memory/` directory (or custom location with `-m`):
- `stepX_search.md`: Raw search results from the crawler agent
- `stepX_analysis.md`: Detailed analysis from the researcher agent
- `stepX_summary.md`: Brief summary of the step's findings

### Output Files (Final Results)

Stored in the `output/` directory (or custom location with `-o`):
- `plan.md`: The research plan (if saved here)
- `stepX.md`: Polished report for each research step
- `summary_final.md`: Overall summary of all research findings

## How It Works

Gizmo uses a multi-agent workflow powered by the Agno framework:

1. **Planning Agent** (GPT-4): Analyzes your prompt and breaks it down into manageable research steps
2. **Crawler Agent** (GPT-3.5): Searches the web for information relevant to each step
3. **Researcher Agent** (GPT-4): Analyzes the search results and produces in-depth findings
4. **Writer Agent** (GPT-3.5): Polishes the researcher's analysis into a well-structured document
5. **Step Summarizer** (GPT-3.5): Creates a concise summary of each step's findings
6. **Final Summarizer** (GPT-4): Synthesizes all step summaries into a comprehensive overview

## Example

1. Create a file `question.txt` with your research prompt:
   ```
   What are the environmental and economic impacts of vertical farming?
   ```

2. Generate a research plan:
   ```bash
   gizmo plan -i question.txt -o plan.md
   ```

3. Execute the research:
   ```bash
   gizmo research -p plan.md -o research_results
   ```

4. Review the results in the `research_results` directory:
   - `step1.md`, `step2.md`, etc.: Detailed reports on each aspect
   - `summary_final.md`: Overall summary of findings

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the environment
- **Rate Limiting**: If you encounter rate limit errors, try running with fewer steps or waiting between runs
- **Memory Usage**: For very large research projects, monitor the `.memory` directory size and clean it if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.
