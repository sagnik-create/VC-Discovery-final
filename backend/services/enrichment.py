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
        # 1️⃣ Cache check
        cached = db.query(EnrichedCompany).filter(EnrichedCompany.url == url).first()
        if cached:
            print("CACHE HIT:", url)
            return {
                "summary": cached.summary,
                "whatTheyDo": cached.whatTheyDo,
                "keywords": cached.keywords,
                "signals": cached.signals,
                "sources": cached.sources,
                "enrichedAt": cached.enrichedAt.isoformat(),  # ✅ always exists
            }

        # 2️⃣ Scrape
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

        # 3️⃣ LLM
        llm_raw = enrich_with_llm(content)
        print("RAW LLM OUTPUT:\n", llm_raw)

        data = extract_json(llm_raw)

        if not data:
            return {
                "summary": "LLM parsing failed",
                "whatTheyDo": [],
                "keywords": [],
                "signals": [],
                "sources": [url],
                "enrichedAt": datetime.utcnow().isoformat(),
            }

        # ✅ Normalize + inject enrichedAt (Option A)
        result = {
            "summary": data.get("summary", ""),
            "whatTheyDo": data.get("whatTheyDo", []),
            "keywords": data.get("keywords", []),
            "signals": data.get("signals", []),
            "sources": data.get("sources", [url]),
            "enrichedAt": datetime.utcnow().isoformat(),
        }

        # 4️⃣ Save to DB
        record = EnrichedCompany(
            url=url,
            summary=result["summary"],
            whatTheyDo=result["whatTheyDo"],
            keywords=result["keywords"],
            signals=result["signals"],
            sources=result["sources"],
            enrichedAt=datetime.utcnow(),  # ✅ ensure DB also has it
        )

        db.add(record)
        db.commit()

        return result

    finally:
        db.close()