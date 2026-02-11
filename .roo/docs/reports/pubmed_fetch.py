"""Minimal PubMed metadata fetcher for research notes.

Usage (PowerShell examples):
  py ./.roo/docs/reports/pubmed_fetch.py --pmids 26052984 23992601
  py ./.roo/docs/reports/pubmed_fetch.py --search "CARMELINA linagliptin JAMA 2019" --retmax 5

Outputs Markdown lines with title, journal/year, PMID, DOI (if present), and PubMed URL.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def _stdout_utf8() -> None:
    # Windows terminals may default to a legacy code page (e.g., cp1252) which
    # can't print some Unicode characters found in PubMed titles.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # py>=3.7
    except Exception:
        pass


def _normalize_text(s: str) -> str:
    # Replace common “invisible” spaces with normal spaces.
    return (
        s.replace("\u2009", " ")  # thin space
        .replace("\u00a0", " ")  # nbsp
        .replace("\u202f", " ")  # narrow nbsp
        .strip()
    )


def _http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "AgentAutoFlow-research/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_pmids(term: str, retmax: int = 10) -> list[str]:
    q = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": term,
            "retmax": str(retmax),
            "retmode": "json",
            "sort": "relevance",
        }
    )
    data = _http_get_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{q}")
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_summaries(pmids: list[str]) -> list[dict]:
    if not pmids:
        return []
    q = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
        }
    )
    data = _http_get_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{q}")
    result = data.get("result", {})
    out = []
    for pmid in pmids:
        rec = result.get(pmid)
        if rec:
            out.append(rec)
    return out


def _extract_doi(articleids: list[dict]) -> str | None:
    for a in articleids or []:
        if a.get("idtype") == "doi":
            return a.get("value")
    return None


def to_md_line(rec: dict) -> str:
    pmid = str(rec.get("uid", ""))
    title = _normalize_text((rec.get("title") or "")).rstrip(".")
    source = rec.get("source")
    pubdate = rec.get("pubdate")
    doi = _extract_doi(rec.get("articleids") or [])
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    bits = [f"- {title}"]
    if source or pubdate:
        bits.append(f"({source}, {pubdate})".replace("(None, ", "(").replace(", None)", ")"))
    bits.append(f"PMID: {pmid}")
    if doi:
        bits.append(f"DOI: {doi}")
    bits.append(url)
    return " ".join(bits)


def main(argv: list[str]) -> int:
    _stdout_utf8()
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pmids", nargs="+", help="PMIDs to fetch")
    g.add_argument("--search", help="PubMed search term")
    ap.add_argument("--retmax", type=int, default=10)
    args = ap.parse_args(argv)

    pmids = args.pmids or search_pmids(args.search, retmax=args.retmax)
    recs = fetch_summaries(pmids)
    for rec in recs:
        print(to_md_line(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

