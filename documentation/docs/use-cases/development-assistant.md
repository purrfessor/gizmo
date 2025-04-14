# Using Gizmo as a Development Assistant

Gizmo can significantly enhance your software development workflow by providing in-depth research and structured guidance for various development tasks. This guide explains how to leverage Gizmo alongside your AI-powered IDE to improve code quality and development efficiency.

## Overview

As a development assistant, Gizmo helps you:

- Research best practices and architectural patterns for your specific development needs
- Break down complex development tasks into manageable steps
- Provide comprehensive context for AI coding assistants
- Create a transparent, step-by-step implementation plan
- Improve the quality and maintainability of your code

## Development Scenarios

Gizmo is particularly valuable in the following development scenarios:

### 1. Service MVP Development

When creating a minimum viable product (MVP) for a new service, Gizmo can:

- Research industry best practices for the specific type of service
- Identify essential features and prioritize development efforts
- Recommend appropriate technology stacks and architectural patterns
- Provide implementation guidance for critical components
- Help establish testing strategies and deployment workflows

### 2. Code Refactoring

For refactoring existing codebases, Gizmo can:

- Analyze current architectural patterns and identify improvement opportunities
- Research modern best practices for the specific technology stack
- Recommend refactoring strategies and patterns
- Break down the refactoring process into manageable steps
- Provide guidance on testing and validating the refactored code

### 3. Feature Development

When adding new features to existing applications, Gizmo can:

- Research similar feature implementations and best practices
- Identify potential integration challenges and solutions
- Recommend appropriate design patterns and approaches
- Provide guidance on testing strategies for the new feature
- Help ensure compatibility with the existing codebase

## Development Workflow

### 1. Formulate Your Development Question

Start by defining a clear, specific question about your development task:

**Examples of good development questions:**
- "What are the best practices for building a Python CLI tool that orchestrates LLM agents?"
- "How should I refactor a monolithic Node.js application into microservices?"
- "What's the most efficient way to implement real-time notifications in a React application?"

### 2. Generate a Research Plan

Use the `plan` command to create a structured research plan:

```bash
gizmo plan -p "Your development question" -o dev_plan.md
```

For complex development tasks, consider using a larger plan size:

```bash
gizmo plan -p "Your development question" -s medium -o dev_plan.md
```

### 3. Execute the Research

Run the research command to gather comprehensive information:

```bash
gizmo research -p dev_plan.md -o dev_research
```

### 4. Integrate with Your AI-Powered IDE

This is where Gizmo's value as a development assistant truly shines:

1. Open your AI-powered IDE (Cursor AI, JetBrains with Junie, VS Code with Copilot, etc.)
2. Share the research results with your AI coding assistant
3. Implement the solution step by step, referencing specific research steps

For example, you might tell your AI assistant:
```
"I've researched how to build a Python CLI tool. Let's implement the command structure described in step1.md in a package called 'cli'."
```

Later, you can continue with:
```
"Now, let's implement the error handling approach described in step4.md."
```

## Benefits of This Approach

Using Gizmo alongside your AI-powered IDE offers several advantages:

1. **Improved Code Quality**: The AI assistant has access to comprehensive research on best practices, resulting in higher-quality code
2. **Structured Implementation**: Breaking down the development process into steps creates a more organized approach
3. **Transparency**: You can track exactly which recommendations are being implemented at each stage
4. **Contextual Awareness**: The AI assistant has full context of the research, enabling more coherent implementation
5. **Learning Opportunity**: You gain insights into best practices while developing your solution

## Example: Refactoring a Python CLI Application

Let's walk through a complete example of using Gizmo to assist with refactoring:

1. **Create a research plan:**
   ```bash
   gizmo plan -p "I'm working on a Python repository that implements a command-line interface (CLI) tool designed to orchestrate local agents that perform deep research tasks using various large language model (LLM) providers. I need to refactor it using best practices for Python CLI development and LLM agent orchestration architecture." -o refactoring_plan.md
   ```

2. **Execute the research:**
   ```bash
   gizmo research -p refactoring_plan.md -o refactoring_research
   ```

3. **Use the research with your AI coding assistant:**
   - Share the research results with your AI assistant
   - Implement the recommended project structure from step1.md
   - Apply the CLI framework recommendations from step2.md
   - Implement the error handling strategies from step4.md
   - Continue through each step until the refactoring is complete

## Tips for Effective Development with Gizmo

- **Be specific about your development context**: Include information about your current tech stack, constraints, and goals
- **Review all research steps before implementation**: Get a complete picture before starting to code
- **Implement incrementally**: Follow the step-by-step approach for more manageable development
- **Iterate as needed**: As you implement, you may discover new questions that require additional research

## Example Prompts

You can find example prompts for different development scenarios in the examples directory of the Gizmo repository:

- Service MVP: `examples/simple/`
- Refactoring: `examples/refactoring/`
- Feature Development: `examples/readme/`

## Related Resources

- [Getting Started with Gizmo](../getting-started.md)
- [Command Reference](../commands/index.md)
- [Plan Command Documentation](../commands/plan.md)
- [Research Command Documentation](../commands/research.md)
