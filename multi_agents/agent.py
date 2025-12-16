"""
LangGraph Multi-Agent Research API

This module exposes the GPT Researcher multi-agent system as a LangGraph graph
that can be deployed to LangGraph Cloud or run locally via `langgraph dev`.

## API Usage

When invoking this graph via the LangGraph API, pass the task configuration
in the `input` parameter:

```python
response = client.runs.create(
    thread_id=thread_id,
    assistant_id="agent",
    input={
        "task": {
            "query": "Your research question here",
            # ... other options below
        }
    }
)
```

## Task Configuration Options

All options have sensible defaults (xAI as default LLM provider).

### Required
- `query` (str): The research question/topic

### Research Configuration  
- `max_sections` (int, default=3): Maximum sections in the report
- `source` (str, default="web"): Research source - "web" or "local"
- `follow_guidelines` (bool, default=False): Whether to follow custom guidelines
- `guidelines` (list[str], default=[]): Custom guidelines for the report
- `include_human_feedback` (bool, default=False): Enable human-in-the-loop review

### LLM Configuration
- `model` (str, default="grok-3-mini"): Model name for multi-agent tasks
- `smart_llm` (str, default="xai:grok-3-mini"): Smart LLM in "provider:model" format
- `fast_llm` (str, default="xai:grok-3-mini"): Fast LLM in "provider:model" format  
- `strategic_llm` (str, default="xai:grok-3-mini"): Strategic LLM for planning

### Output Configuration
- `publish_formats` (dict): Output formats {"markdown": true, "pdf": true, "docx": true}
- `verbose` (bool, default=True): Enable verbose logging

### Advanced Options
- `tone` (str, default="Objective"): Report tone
- `max_search_results` (int, default=5): Max search results per query
- `max_subtopics` (int, default=3): Max subtopics to research
- `language` (str, default="english"): Report language
- `report_format` (str, default="APA"): Citation format

## Example - Full Configuration

```python
{
    "task": {
        "query": "What are the latest developments in quantum computing?",
        "max_sections": 4,
        "source": "web",
        "model": "grok-3-mini",
        "smart_llm": "xai:grok-3-mini",
        "follow_guidelines": True,
        "guidelines": [
            "Focus on practical applications",
            "Include recent 2024 developments"
        ],
        "publish_formats": {
            "markdown": True,
            "pdf": True,
            "docx": False
        },
        "verbose": True,
        "language": "english",
        "report_format": "APA"
    }
}
```

## Environment Variables

The following env vars configure API keys and default providers:

- OPENAI_API_KEY: OpenAI API key
- XAI_API_KEY: xAI/Grok API key  
- TAVILY_API_KEY: Tavily search API key
- SMART_LLM: Default smart LLM (e.g., "xai:grok-3-mini")
- FAST_LLM: Default fast LLM
- RETRIEVER: Search retriever (default: "tavily")
"""

import os
from multi_agents.agents import ChiefEditorAgent

# Default task configuration with xAI as the default provider
DEFAULT_TASK = {
    # Research settings
    "query": "What is the current state of AI?",  # Placeholder - should be overridden
    "max_sections": 3,
    "source": "web",
    "follow_guidelines": False,
    "guidelines": [],
    "include_human_feedback": False,
    
    # LLM settings - xAI Grok as default
    "model": os.getenv("SMART_LLM_MODEL", "grok-3-mini"),
    
    # Output settings
    "publish_formats": {
        "markdown": True,
        "pdf": True,
        "docx": True
    },
    "verbose": True,
    
    # Advanced settings
    "language": "english",
    "report_format": "APA",
    "tone": "Objective",
}

# Create the chief editor with default task
# The actual task will be passed via API input and merged with defaults
chief_editor = ChiefEditorAgent(
    task=DEFAULT_TASK,
    websocket=None,
    stream_output=None
)

# Initialize and compile the research graph
graph = chief_editor.init_research_team()
graph = graph.compile()