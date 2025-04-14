# Using Gizmo as a Development Assistant

Gizmo can significantly enhance your software development workflow by providing in-depth research and structured guidance for various development tasks. This guide explains how to leverage Gizmo alongside your AI-powered IDE to streamline your development process and reduce routine work.

## Overview

As a development assistant, Gizmo helps you:

- Research best practices and architectural patterns for your specific development needs
- Break down complex development tasks into manageable steps
- Provide comprehensive context for AI coding assistants
- Create a transparent, step-by-step implementation plan
- Improve the quality and maintainability of your code

## Development Workflow

The Gizmo development assistant workflow consists of five straightforward steps:

### 1. Formulate Your Development Question

Start by defining a clear, specific question about your development task. Your question should focus on what you're trying to accomplish.

**Example prompts for different scenarios:**

**For developing an MVP for a new service:**
- "What's the best architecture for a scalable e-commerce microservice in Go?"
- "How should I design a Python API service for processing and analyzing user-generated content?"
- "What are the essential components for a real-time chat application using Node.js and WebSockets?"

**For developing a new feature in an existing service:**
- "How can I implement a recommendation system in my existing e-commerce platform?"
- "What's the best approach to add multi-factor authentication to my Java web application?"
- "How should I implement a rate-limiting mechanism in my REST API service?"

**For performing a refactoring on a service:**
- "How can I refactor my monolithic PHP application into a microservices architecture?"
- "What's the best way to migrate my application from REST to GraphQL?"
- "How should I modernize my legacy jQuery codebase to use React and TypeScript?"

### 2. Create/Open a Project in Your IDE

Open your preferred IDE (VS Code, JetBrains IDEs, Cursor, etc.) and either:

- Create a new project for your development task
- Open an existing project that you want to enhance or refactor

### 3. Create a Plan Using Gizmo CLI

Use the `plan` command to create a structured development plan:

```bash
gizmo plan -p "Your development question" -o {project_dir}/todo/dev_plan.md
```

For complex development tasks, consider using a larger plan size:

```bash
gizmo plan -p "Your development question" -s medium -o {project_dir}/todo/dev_plan.md
```

This plan will break down your development task into logical, manageable steps.

### 4. Perform Research with Output into Your Repository

Run the research command to gather comprehensive information about each step in your plan:

```bash
gizmo research -p {project_dir}/todo/dev_plan.md -o {project_dir}/todo/dev_research
```

Gizmo will:
- Search for best practices, design patterns, and implementation approaches
- Analyze and synthesize the information
- Create detailed reports for each step in your development plan
- Generate a comprehensive summary of all findings

All this information will be saved directly in your project repository, making it easily accessible.

### 5. Leverage Your AI Assistant in the IDE

This is where the magic happens:

1. In your IDE, use your AI coding assistant (GitHub Copilot, JetBrains AI Assistant, Cursor AI, etc.)
2. Prompt the AI assistant to read and utilize the research documents

For example, you might tell your AI assistant:

```
"Please read the files in the dev_research directory and help me implement the collaborative filtering approach described in step2.md."
```

Or:

```
"Based on the microservices architecture research in dev_research/step1.md, help me refactor this user authentication module into a separate microservice."
```

Your AI assistant can now provide much more targeted, high-quality guidance based on the comprehensive research Gizmo has performed.

## Benefits for Developers

This workflow addresses many common pain points in a developer's daily routine:

1. **Reduces Research Time**: No more jumping between Stack Overflow, documentation, and blog posts
2. **Provides Structured Guidance**: Transforms vague requirements into clear, actionable steps
3. **Enhances AI Coding Assistants**: Gives your AI assistant the context it needs to provide truly helpful code suggestions
4. **Improves Code Quality**: Ensures implementations follow best practices and established patterns
5. **Accelerates Onboarding**: Helps developers quickly understand new technologies or domains
6. **Creates Documentation**: The research outputs serve as documentation for implementation decisions

## Example: Developing a New Feature

Let's walk through a complete example of using Gizmo to assist with adding a new feature:

1. **Formulate your question:**
   "How should I implement a user notification system with both in-app and email notifications in my React/Node.js application?"

2. **Open your project in your IDE:**
   Open your React/Node.js application in Cursor, WebStorm, or another IDE.

3. **Create a research plan:**
   ```bash
   gizmo plan -p "How should I implement a user notification system with both in-app and email notifications in an React/Node.js application?" -o {project_dir}/todo/notification_plan.md
   ```
   
   If necessary, you can also ask your AI assistant in IDE to write some description of the project in an `.md` file so that gizmo can use that file as an input to have more context about your project. For example tell Cursor:
     "Write a brief description of the service including the technology stack, main functionalities and architecture. Put it into a file `prompt.md`." Then add additional instruction into the `prompt.md` if needed, and call:

   ```bash
   gizmo plan -i {project_dir}/todo/prompt.md -o {project_dir}/todo/notification_plan.md
   ```

4. **Execute the research:**
   ```bash
   gizmo research -p {project_dir}/todo/notification_plan.md -o {project_dir}/todo
   ```

5. **Use your AI assistant in the IDE:**
   Prompt your AI assistant: "I need to implement a notification system in my app. Please read the research in the todo directory and help me implement the notification service backend described in step2.md."

## Tips for Effective Development with Gizmo

- **Be specific about your tech stack**: Include information about frameworks, libraries, and versions you're using
- **Specify constraints**: Mention any performance requirements, compatibility needs, or other limitations
- **Start with architecture**: Implement high-level architectural recommendations before diving into specific components
- **Commit research to version control**: The research documents are valuable references for future development
- **Iterate as needed**: As you implement, you may discover new questions that require additional research

## Related Resources

- [Getting Started with Gizmo](../getting-started.md)
- [Command Reference](../commands/index.md)
- [Plan Command Documentation](../commands/plan.md)
- [Research Command Documentation](../commands/research.md)
