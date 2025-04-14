# Observability

Gizmo provides observability features to help you monitor resource usage and costs during your research projects. This guide explains how Gizmo tracks and reports token usage and estimated costs.

## Token Usage Tracking

Gizmo tracks the total number of tokens used throughout the research process. Tokens are the basic units of text that language models process, and they directly impact the cost of using the OpenAI API.

The token tracking system works differently depending on the research mode:

### Regular Research Mode

In regular research mode:
- Gizmo accumulates tokens used across all steps of the research process
- At the end of the research, it prints the total number of tokens used
- Example output: `Total tokens used: 25430`
- It also logs the total model time: `Total model time: 12.3456s`

### Deep Research Mode

In deep research mode:
- Gizmo uses the GPT Researcher library for more comprehensive research
- It tracks both the tokens used by GPT Researcher and other components
- At the end of each research step, it prints the estimated cost in USD: `GPT Researcher costs: 0.1234$`
- At the end of the research, it prints the total tokens used for components other than GPT Researcher

## Cost Estimation

While exact costs depend on the OpenAI API pricing at the time of usage, Gizmo provides approximate cost estimates to help you budget your research:

| Research Type | Size | Estimated Cost |
|---------------|------|----------------|
| Regular Research | Small (1-10 steps) | ~$0.05-0.10    |
| Regular Research | Medium (10-30 steps) | ~$0.10-0.30    |
| Regular Research | Large (30-70 steps) | ~$0.30-0.70    |
| Deep Research | Small (1-10 steps) | ~$0.20-0.50    |
| Deep Research | Medium (10-30 steps) | ~$0.50-3.50    |
| Deep Research | Large (30-70 steps) | ~$3.50-...     |

**Note that this is a very rough estimate that should give you a general understanding of how much approximately it might cost to run one research**

These estimates are based on typical usage patterns and may vary depending on:
- The complexity of your research topic
- The number of search results processed
- The length of generated reports
- Current OpenAI API pricing

## Implementation Details

Gizmo implements token tracking using the `UsageAccumulator` class, which:
- Records metrics from each agent run
- Accumulates total tokens used and model time
- Provides methods to retrieve the accumulated metrics

For deep research, Gizmo leverages the cost tracking features of the GPT Researcher library, which calculates costs based on the specific models used during the research process.

## Best Practices

To optimize costs when using Gizmo:

1. **Start with smaller research plans**: Use the `-s small` option when creating research plans to limit the number of steps
2. **Be specific with your research questions**: More focused questions typically require fewer tokens to research
3. **Use regular research for initial exploration**: Start with regular research and only use deep research when necessary
4. **Monitor token usage**: Pay attention to the token usage reports to identify patterns and optimize future research
5. **Set budget limits**: Decide on a budget before starting extensive research projects

## Example Output

### Regular Research Output
```
Research completed in 45.67s total!
Total steps processed: 7
Total tokens used: 25430
Total model time: 12.3456s
```

### Deep Research Output
```
GPT Researcher costs: 0.1234$
Research completed in 78.90s total!
Total steps processed: 7
Total tokens used: 8765
Total model time: 5.6789s
```

The token usage information helps you understand the resources consumed by your research and estimate costs for future projects.
