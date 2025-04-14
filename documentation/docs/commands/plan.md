# `plan` Command

The `plan` command is the first step in the Gizmo research workflow. It analyzes your research question or topic and generates a structured research plan that breaks down the topic into manageable steps.

## Syntax

```bash
gizmo plan [-i <input_file> | -p <prompt>] [-s <size>] [-o <output_file>]
```

## Description

When you run the `plan` command, Gizmo uses AI to:

1. Analyze your research question
2. Identify the key aspects that need to be investigated
3. Create a logical sequence of research steps
4. Generate a structured plan in Markdown format

The resulting research plan serves as a roadmap for the subsequent `research` command, ensuring that your topic is explored thoroughly and systematically.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Path to a text file containing your research question | None |
| `-p, --prompt` | Type your research question directly in the command | None |
| `-s, --size` | Size of the research plan: `small` (1-10 steps), `medium` (10-30 steps), `large` (30-70 steps) | `small` |
| `-o, --output` | Where to save your research plan | `plan.md` in the current directory |

**Note**: You must provide either `-i` or `-p` to specify your research question.

## Examples

### Basic Usage

```bash
# Using a prompt directly in the command:
gizmo plan -p "What are the environmental impacts of vertical farming?" -o farming_plan.md

# Using a question from a file:
gizmo plan -i my_question.txt -o research_plan.md
```

### Adjusting Plan Size

For more complex topics, you can specify the size of your research plan:

```bash
# For a medium-sized research plan (10-30 steps):
gizmo plan -p "How do different dog breeds compare as family pets?" -s medium -o dog_plan.md

# For a large, comprehensive research plan (30-70 steps):
gizmo plan -p "What are effective study techniques for college students?" -s large -o study_plan.md
```

## Output

The `plan` command generates a Markdown file containing:

- Your original research question
- A structured list of research steps
- Brief descriptions of what each step will investigate

Example output structure:

```markdown
# Research Plan: What are the environmental impacts of vertical farming?

## Research Steps:

### 1. Define vertical farming and its key characteristics
   - Investigate the definition and basic concepts of vertical farming
   - Identify the main types and approaches to vertical farming

### 2. Examine water usage in vertical farming
   - Compare water consumption between vertical farming and traditional agriculture
   - Analyze water recycling and conservation techniques in vertical farming systems

[Additional steps...]
```

## After Creating Your Plan

After generating your research plan, you can:

1. **Review the plan**: Open the output file to examine the research steps
   ```bash
   cat farming_plan.md
   ```

2. **Edit if needed**: Modify the plan to better suit your research needs
   ```bash
   nano farming_plan.md  # or use your preferred text editor
   ```

3. **Execute the research**: Use the [`research`](research.md) command to start the research process
   ```bash
   gizmo research -p farming_plan.md -o farming_results
   ```

## Related Commands

- [`research`](research.md) - Execute the research based on the generated plan
