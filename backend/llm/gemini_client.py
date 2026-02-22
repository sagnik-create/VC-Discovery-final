import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")

def enrich_with_llm(text: str):
    prompt = f"""
You are a VC research assistant.

Extract the following fields from the website content:

- summary (string)
- whatTheyDo (array of strings)
- keywords (array of strings)
- signals (array of strings)
- sources (array of urls or strings)

Return ONLY valid JSON.
Do NOT wrap in markdown.
Do NOT add explanations.
Do NOT add backticks.

Website Content:
{text[:6000]}
"""
    response = model.generate_content(prompt)
    return response.text