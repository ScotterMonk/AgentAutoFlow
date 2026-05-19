"""Call a Hermes agent via the local API."""
import requests
import json

HERMES_API_URL = os.getenv("HERMES_API_URL")
HERMES_API_KEY = os.getenv("HERMES_API_KEY")

# ── Configuration ───────────────────────────────────────────
# FUTURE: If a dedicated scraper agent profile exists in Hermes,
# change MODEL below to that profile name (e.g., "scraper").
# This routes all calls to the specialist instead of the default.
MODEL = "hermes-agent"
# ─────────────────────────────────────────────────────────────

def query_hermes(prompt: str, timeout: int = 300) -> str:
    """Send a query to Hermes, return the response.

    Args:
        prompt: The task. Be specific — "No extra text, just JSON"
                if you need parseable output.
        timeout: Seconds. Browser tasks need 120-300s. Simple
                 searches need 30s.

    Returns:
        Hermes agent's text response.
    """
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def scrape(url: str, fields: str, *, site: str | None = None) -> list[dict]:
    """Convenience: scrape structured data from a URL.

    Args:
        url: Page to scrape.
        fields: Comma-separated field names (e.g., "name,date,location").
        site: Optional site name for credential lookup
              (e.g., "athletic.net", "amazon").

    Returns:
        List of dicts with the requested fields.
    """
    login = f"Log into {site}. " if site else ""
    prompt = (
        f"{login}Navigate to {url} and extract ONLY these fields "
        f"as a clean JSON array: {fields}. "
        f"No extra text, no markdown, no explanation. Just the JSON array."
    )
    return json.loads(query_hermes(prompt))
