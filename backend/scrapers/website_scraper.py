import requests
from bs4 import BeautifulSoup


def scrape_website(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove junk
        for tag in soup(["script", "style", "noscript", "header", "footer", "svg"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)
        return text[:8000]  # limit size for LLM later

    except Exception as e:
        print("Scraping failed:", e)
        return ""