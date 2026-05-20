---
name: hermes-api-client
description: >
  Call a Hermes agent from Kilo Code via the local chat completions API.
  Use for web scraping, browser automation, and research tasks that
  Hermes handles better (saved credentials, browser tools, web search).
modes:
  - name: scrape
    description: Extract structured JSON data from a website
    template: |
      Navigate to {url}. {login clause}. Extract ONLY {fields} as a
      clean JSON array. No extra text, no markdown. Just the JSON.
  - name: research
    description: Web research and synthesis
    template: |
      Research {topic}. Be thorough but concise. Use web search.
  - name: browser
    description: Full browser automation — login, navigate, act
    template: |
      Log into {site} as {email}. Navigate to {target}. {action}.
      Return results as clean JSON. No extra text.
  - name: extract
    description: Pull specific named fields from a page
    template: |
      Go to {url} and extract ONLY these fields as JSON: {fields}.
      No other text.
---

# Hermes API Client — Kilo Code Skill

Call a Hermes agent from Kilo Code. Hermes may have browser tools, web search, and saved site credentials that Kilo Code lacks. Delegate scraping/browsing/research tasks via a single Python function. Read skill-local guidance only when `.kilocode/skills/hermes-api-client/AGENTS.md` is confirmed to exist; otherwise use root `AGENTS.md` for project-specific gateway, host, credential, and site notes.

## Prerequisites

- Hermes gateway available and reachable
- Python 3 + `requests` installed (`pip install requests`)

## The Tool Script

Use `.kilocode/skills/hermes-api-client/scripts/hermes_api.py`. When importing it from a project-root script, add `.kilocode/skills/hermes-api-client/scripts` to `sys.path` or run a small wrapper from that directory.

## Modes

### Mode 1 — Scrape (structured data extraction)

```python
from hermes_api import query_hermes
import json

result = query_hermes(
    "Navigate to https://example.com/events, find all upcoming "
    "events, return ONLY a clean JSON array with fields: "
    "title, date, venue. No extra text."
)
data = json.loads(result)
```

Or use the convenience wrapper:

```python
from hermes_api import scrape

meets = scrape(
    "https://example.com/...",
    fields="name,date,location",
    site="example.com",
)
```

### Mode 2 — Research

```python
result = query_hermes(
    "Research the current state of WebGPU in Electron. "
    "Be thorough but concise."
)
# result is plain text / markdown
```

### Mode 3 — Browser Automation

```python
result = query_hermes(
    "Log into amazon.com as user@email.com, navigate to order "
    "history, return last 5 orders as JSON with fields: "
    "item, price, status, date. No extra text."
)
```

### Mode 4 — Field Extraction

```python
result = query_hermes(
    "Go to https://example.com/product/123 and extract ONLY "
    "these fields as JSON: price, in_stock, sku. No other text."
)
```

## Quick Reference

**Get prices from X** — Use scrape mode with `scrape(url, fields, site=...)`.
**What's the best way to…** — Use research mode with `query_hermes("Research …")`.
**Log into X and download…** — Use browser mode with `query_hermes("Log into X …")`.
**Pull the author from…** — Use extract mode with `query_hermes("Extract fields: …")`.

## Error Handling

```python
try:
    data = scrape("https://example.com/data", "name,price")
except requests.Timeout:
    # Site slow, CAPTCHA, Cloudflare block
    print("Hermes timed out — try longer timeout or simpler query")
except requests.HTTPError as e:
    print(f"API error {e.response.status_code}: {e.response.text}")
except json.JSONDecodeError:
    # Prompt likely missing "No extra text, just the JSON"
    print(f"Hermes returned non-JSON. Add stricter prompt.")
```

## Future Customization Points

**1. Dedicated scraper agent** — If you create a Hermes profile just
for scraping, change `MODEL` in the script:

```python
# Before (default agent):
MODEL = "hermes-agent"

# After (dedicated scraper profile):
MODEL = "scraper"
```

**2. Different Hermes host** — If the gateway moves:

```python
API_URL = "http://other-host:8642/v1/chat/completions"
```

**3. Streaming responses** — For long tasks, switch to `stream: True`
and process chunks. See OpenAI streaming docs for pattern.

**4. Multiple agents** — If you have separate agents for separate sites:

```python
MODEL_MAP = {
    "example.com": "example-scraper",
    "shopping-site": "shopping-scraper",
    "default": "hermes-agent",
}

def scrape(url, fields, site=None):
    model = MODEL_MAP.get(site, MODEL_MAP["default"])
    return query_hermes(prompt, model=model)  # add model param
```

## Tips

1. **"No extra text, just the JSON"** — non-negotiable for parseable
   output. Hermes agents are chatty otherwise.
2. **One task per call** — don't ask for two different sites in one
   prompt. Split into separate `query_hermes()` calls.
3. **Be specific about fields** — `"name,date,location"` beats
   `"give me all the details"`.
4. **Timeout wisely** — browser tasks: 120-300s. Simple API calls: 30s.
5. **Site credentials live in Hermes** — Kilo Code doesn't need them.
   Hermes agents have saved logins for sites they're configured for.
