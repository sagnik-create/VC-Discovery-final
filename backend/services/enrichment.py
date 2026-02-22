import json
import re
from datetime import datetime
from scrapers.website_scraper import scrape_website
from llm.gemini_client import enrich_with_llm
from db import SessionLocal, EnrichedCompany


def extract_json(text: str):
    """
    Extract first JSON object from LLM output safely.
    """
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except Exception as e:
        print("JSON parse error:", e)
        return None


def enrich_company_from_url(url: str):
    db = SessionLocal()

    try:
        cached = db.query(EnrichedCompany).filter(EnrichedCompany.url == url).first()
        if cached:
            return {
                "summary": cached.summary,
                "whatTheyDo": json.loads(cached.whatTheyDo),
                "keywords": json.loads(cached.keywords),
                "signals": json.loads(cached.signals),
                "sources": json.loads(cached.sources),
                "enrichedAt": cached.enrichedAt.isoformat(),
            }

        content = scrape_website(url)
        if not content:
            return {
                "summary": "Could not scrape website",
                "whatTheyDo": [],
                "keywords": [],
                "signals": [],
                "sources": [url],
                "enrichedAt": datetime.utcnow().isoformat(),
            }

        llm_raw = enrich_with_llm(content)
        data = extract_json(llm_raw)

        if not data:
            return {
                "summary": "LLM parsing failed",
                "whatTheyDo": [],
                "keywords": [],
                "keywords": [],
                "signals": [],
                "sources": [url],
                "enrichedAt": datetime.utcnow().isoformat(),
            }

        result = {
            "summary": data.get("summary", ""),
            "whatTheyDo": data.get("whatTheyDo", []),
            "keywords": data.get("keywords", []),
            "signals": data.get("signals", []),
            "sources": data.get("sources", [url]),
            "enrichedAt": datetime.utcnow().isoformat(),
        }

        record = EnrichedCompany(
            url=url,
            summary=result["summary"],
            whatTheyDo=json.dumps(result["whatTheyDo"]),
            keywords=json.dumps(result["keywords"]),
            signals=json.dumps(result["signals"]),
            sources=json.dumps(result["sources"]),
        )

        db.add(record)
        db.commit()
        return result

    except Exception as e:
        print("ENRICH ERROR:", e)
        return {
            "summary": "Enrichment failed in production",
            "whatTheyDo": [],
            "keywords": [],
            "signals": [],
            "sources": [url],
            "enrichedAt": datetime.utcnow().isoformat(),
        }
    finally:
        db.close()