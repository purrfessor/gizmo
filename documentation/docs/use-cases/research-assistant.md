# Using Gizmo as a Research Assistant

Gizmo excels as a research assistant, helping you explore any topic thoroughly and efficiently. This guide explains how to leverage Gizmo's capabilities to conduct comprehensive research on various subjects.

## Overview

As a research assistant, Gizmo:

- Breaks down complex research topics into manageable steps
- Searches the internet for relevant, up-to-date information
- Analyzes and synthesizes findings from multiple sources
- Maintains context across the entire research process
- Delivers well-organized, readable reports

## When to Use Gizmo for Research

Gizmo is ideal for research tasks such as:

- **Academic Research**: Literature reviews, background research for papers, exploring new fields
- **Professional Research**: Market analysis, competitive intelligence, industry trends
- **Personal Learning**: Exploring new hobbies, planning trips, investigating health topics
- **Decision Support**: Gathering information to make informed choices about products, services, or life decisions (like buying an apartment)

## Research Workflow

### 1. Formulate Your Research Question

Start by defining a clear, specific research question. The more focused your question, the more targeted Gizmo's research will be.

**Examples of good research questions:**
- "What are the environmental and economic impacts of vertical farming?"
- "How do different approaches to intermittent fasting affect metabolic health?"
- "What are the most effective teaching methods for introducing programming to children ages 8-12?"

### 2. Generate a Research Plan

Use the `plan` command to create a structured research plan:

```bash
gizmo plan -p "Your research question" -o research_plan.md
```

Gizmo will analyze your question and break it down into logical research steps. For complex topics, consider using the medium or large plan size:

```bash
gizmo plan -p "Your research question" -s medium -o research_plan.md
```

### 3. Review and Refine the Plan

Open the generated plan file and review it:

```bash
cat research_plan.md
```

You can edit the plan if needed to better align with your research goals:

```bash
nano research_plan.md  # or use your preferred text editor
```

### 4. Execute the Research

Run the research command to start the information gathering process:

```bash
gizmo research -p research_plan.md -o results_directory
```

Gizmo will:
- Search the internet for information related to each step in your plan
- Analyze and synthesize the findings
- Create detailed reports for each research step
- Generate a comprehensive summary

### 5. Review and Use the Results

Navigate to your results directory to explore the findings:

```bash
cd results_directory
```

Key files to review:
- `summary_final.md`: Start here for a comprehensive overview of all findings
- `step1.md`, `step2.md`, etc.: Detailed reports for each research step

## Example: Researching Renewable Energy

Let's walk through a complete example of using Gizmo to research renewable energy technologies:

1. **Create a research plan:**
   ```bash
   gizmo plan -p "What are the most promising renewable energy technologies for residential use in 2023?" -o energy_plan.md
   ```

2. **Execute the research:**
   ```bash
   gizmo research -p energy_plan.md -o energy_research
   ```

3. **Review the results:**
   The `energy_research` directory will contain:
   - Reports on different renewable technologies (solar, wind, geothermal, etc.)
   - Comparisons of cost, efficiency, and practicality
   - Analysis of installation and maintenance requirements
   - Summary of the most promising options for residential use

## Tips for Effective Research with Gizmo

- **Be specific**: Narrow research questions yield more focused results
- **Use appropriate plan sizes**: Match the plan size to the complexity of your topic
- **Review intermediate results**: Check individual step reports for detailed information
- **Save your research**: Keep your research outputs for future reference
- **Iterate if needed**: Run additional research to explore specific aspects in more depth

## Related Resources

- [Getting Started with Gizmo](../getting-started.md)
- [Command Reference](../commands/index.md)
- [Plan Command Documentation](../commands/plan.md)
- [Research Command Documentation](../commands/research.md)
