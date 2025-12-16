# GPT Researcher API Documentation

## Base URL

```
https://web-production-6dd8.up.railway.app
```

---

## Endpoint: Run Multi-Agent Research

### `POST /api/research`

Conducts comprehensive multi-agent research on any topic and returns a structured report with citations.

### Request

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | — | The research question or topic |
| `max_sections` | integer | No | `3` | Number of sections in the report (1-10) |
| `model` | string | No | `"xai:grok-3-mini"` | LLM model in `provider:model` format |
| `source` | string | No | `"web"` | Research source: `"web"` or `"local"` |
| `language` | string | No | `"english"` | Output language |
| `report_format` | string | No | `"APA"` | Citation format: `"APA"`, `"MLA"`, `"Chicago"`, `"Harvard"` |
| `follow_guidelines` | boolean | No | `false` | Whether to follow custom guidelines |
| `guidelines` | array | No | `[]` | List of custom guidelines (strings) |
| `verbose` | boolean | No | `true` | Enable detailed logging |

### Supported Models

| Provider | Model | Format |
|----------|-------|--------|
| xAI | Grok 3 Mini | `"xai:grok-3-mini"` |
| xAI | Grok 3 | `"xai:grok-3"` |
| OpenAI | GPT-4o | `"openai:gpt-4o"` |
| OpenAI | GPT-4o Mini | `"openai:gpt-4o-mini"` |
| Anthropic | Claude 3.5 Sonnet | `"anthropic:claude-3-5-sonnet-20241022"` |

### Response

**Success (200):**

```json
{
  "success": true,
  "query": "What are the best practices for API authentication?",
  "title": "Best Practices for API Authentication",
  "report": "# Best Practices for API Authentication\n\n## Introduction\n\n...(full markdown report)...",
  "sources": [
    "https://example.com/article1",
    "https://example.com/article2"
  ]
}
```

**Error (500):**

```json
{
  "detail": "Research failed: <error message>"
}
```

---

## Examples

### Minimal Request (Python)

```python
import requests

response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "What are the emerging trends in renewable energy for 2025?"
    },
    timeout=300  # Research can take 2-5 minutes
)

result = response.json()
print(result["report"])
```

### Full Request (Python)

```python
import requests

response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "Compare React, Vue, and Angular for enterprise applications",
        "max_sections": 5,
        "model": "xai:grok-3-mini",
        "language": "english",
        "report_format": "APA",
        "follow_guidelines": True,
        "guidelines": [
            "Focus on performance and scalability",
            "Include code examples where relevant",
            "Consider enterprise support and ecosystem"
        ]
    },
    timeout=300
)

if response.status_code == 200:
    result = response.json()
    print(f"Title: {result['title']}")
    print(f"Sources used: {len(result['sources'])}")
    print(result["report"])
else:
    print(f"Error: {response.json()['detail']}")
```

### cURL Example

```bash
curl -X POST "https://web-production-6dd8.up.railway.app/api/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current state of quantum computing?",
    "max_sections": 3
  }'
```

### JavaScript/Node.js Example

```javascript
const response = await fetch("https://web-production-6dd8.up.railway.app/api/research", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    query: "Best practices for microservices architecture",
    max_sections: 4,
    model: "xai:grok-3-mini"
  })
});

const result = await response.json();
console.log(result.report);
```

---

## Important Notes

### Timeout
- Research typically takes **2-5 minutes** depending on query complexity
- Set HTTP timeout to at least **300 seconds (5 minutes)**
- Complex queries with more sections take longer

### Rate Limits
- No built-in rate limiting, but be reasonable
- Each request triggers multiple web searches and LLM calls

### Report Output
- The `report` field contains **full Markdown** with headers, lists, citations
- Parse as Markdown for rendering
- Sources are included both inline (as citations) and in the `sources` array

### Error Handling
- 500 errors include details in the `detail` field
- Common issues: LLM provider errors, search failures, timeout
- Implement retry logic for production use

---

## Health Check

### `GET /`

Returns basic server info to verify the API is running.

```bash
curl https://web-production-6dd8.up.railway.app/
```

---

## Architecture

This API uses a **multi-agent system** with specialized AI agents:

1. **Chief Editor** - Orchestrates the research process
2. **Researcher** - Conducts web searches and gathers sources
3. **Editor** - Plans report structure and sections
4. **Writer** - Generates content for each section
5. **Reviewer** - Reviews and critiques the draft
6. **Revisor** - Improves content based on feedback
7. **Publisher** - Formats the final report

The system uses:
- **Serper** for Google search (retriever)
- **Firecrawl** for content extraction (scraper)
- **xAI Grok** as the default LLM (configurable)
