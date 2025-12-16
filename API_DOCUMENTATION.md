# GPT Researcher API Documentation

## Base URL

```
https://web-production-6dd8.up.railway.app
```

---

## Endpoint: Run Research

### `POST /api/research`

Conducts research on any topic and returns a structured report with citations.

### Report Types

| Type | Value | Speed | Best For |
|------|-------|-------|----------|
| **Summary** | `research_report` | ~2 min | Quick answers, overviews |
| **Detailed** | `detailed_report` | ~5 min | In-depth single-topic research |
| **Resource** | `resource_report` | ~3 min | Curated list of sources |
| **Deep** | `deep` | ~10+ min | Exhaustive recursive research |
| **Multi-Agent** | `multi_agents` | ~5-10 min | Comprehensive reports with multiple AI agents |

---

### Request

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ Yes | — | The research question or topic |
| `report_type` | string | No | `"research_report"` | Type of report (see table above) |
| `report_source` | string | No | `"web"` | Source: `"web"` or `"local"` |
| `tone` | string | No | `"Objective"` | Writing tone (see tones below) |

**Multi-Agent Only Parameters** (when `report_type="multi_agents"`):

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_sections` | integer | `3` | Number of report sections (1-10) |
| `language` | string | `"english"` | Output language |
| `report_format` | string | `"APA"` | Citation format |
| `follow_guidelines` | boolean | `false` | Use custom guidelines |
| `guidelines` | array | `[]` | Custom guideline strings |

### Available Tones

`Objective`, `Formal`, `Analytical`, `Persuasive`, `Informative`, `Explanatory`, `Descriptive`, `Critical`, `Comparative`, `Speculative`, `Reflective`, `Narrative`, `Humorous`, `Optimistic`, `Pessimistic`, `Simple`, `Casual`

---

### Response

**Success (200):**

```json
{
  "success": true,
  "query": "What is quantum computing?",
  "report_type": "research_report",
  "report": "# Quantum Computing\n\n...(full markdown report)...",
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

### Quick Summary (Fastest)

```python
import requests

response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "What are the benefits of meditation?",
        "report_type": "research_report"
    },
    timeout=180
)

print(response.json()["report"])
```

### Detailed Report

```python
response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "Compare PostgreSQL vs MongoDB for web applications",
        "report_type": "detailed_report",
        "tone": "Analytical"
    },
    timeout=300
)
```

### Multi-Agent (Most Comprehensive)

```python
response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "The future of renewable energy in 2025",
        "report_type": "multi_agents",
        "max_sections": 5,
        "language": "english",
        "report_format": "APA"
    },
    timeout=600
)
```

### Deep Research (Most Exhaustive)

```python
response = requests.post(
    "https://web-production-6dd8.up.railway.app/api/research",
    json={
        "query": "Complete guide to machine learning algorithms",
        "report_type": "deep"
    },
    timeout=900  # Can take 10-15 minutes
)
```

### cURL Example

```bash
curl -X POST "https://web-production-6dd8.up.railway.app/api/research" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current state of AI?",
    "report_type": "research_report"
  }'
```

### JavaScript/Node.js Example

```javascript
const response = await fetch("https://web-production-6dd8.up.railway.app/api/research", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "Best practices for API security",
    report_type: "detailed_report"
  })
});

const result = await response.json();
console.log(result.report);
```

---

## Choosing the Right Report Type

| Use Case | Recommended Type | Why |
|----------|------------------|-----|
| Quick fact check | `research_report` | Fast, concise |
| Blog post research | `detailed_report` | Thorough, single-agent |
| Finding resources | `resource_report` | Curated source list |
| Academic paper | `multi_agents` | Multiple perspectives, citations |
| Comprehensive guide | `deep` | Recursive, exhaustive |

---

## Important Notes

### Timeouts
- `research_report`: 2-3 minutes → timeout 180s
- `detailed_report`: 4-6 minutes → timeout 300s
- `multi_agents`: 5-10 minutes → timeout 600s
- `deep`: 10-20 minutes → timeout 900s+

### Rate Limits
- No built-in rate limiting
- Each request triggers multiple web searches and LLM calls
- Be reasonable with concurrent requests

### Report Output
- The `report` field contains **full Markdown**
- Parse as Markdown for rendering
- Sources included in `sources` array

---

## Health Check

### `GET /`

Returns basic server info.

```bash
curl https://web-production-6dd8.up.railway.app/
```

---

## Architecture

**Single-Agent Reports** (`research_report`, `detailed_report`, `resource_report`, `deep`):
- One GPT Researcher agent handles the entire workflow
- Searches → Scrapes → Analyzes → Writes

**Multi-Agent Reports** (`multi_agents`):
- 7 specialized AI agents collaborate:
  1. Chief Editor (orchestration)
  2. Researcher (web search)
  3. Editor (structure planning)
  4. Writer (content generation)
  5. Reviewer (quality check)
  6. Revisor (improvements)
  7. Publisher (final formatting)

**Infrastructure:**
- Serper (Google search)
- Firecrawl (content extraction)
- xAI Grok (default LLM)
