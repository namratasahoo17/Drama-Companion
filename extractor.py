"""Text extraction utilities for review and preference data."""

import json
from llm import ask_gemini


def _clean_json_response(response: str) -> str:
    """Strip Markdown fencing and whitespace from model output."""
    return response.replace("```json", "").replace("```", "").strip()


def extract_review(review_text: str) -> dict:
    """Extract a structured review object from free-form text."""
    prompt = f"""
Extract the following into JSON.
Review: {review_text}
Return only valid JSON matching this schema:
{{
  "title": "",
  "overall_rating": 0,
  "aspects": [
    {{
      "name": "",
      "score": 0,
      "reason": ""
    }}
  ]
}}
"""
    response = ask_gemini(prompt)
    response = _clean_json_response(response)
    return json.loads(response)


def extract_preferences(review_text: str, category_text: str) -> list:
    """Extract user preference records from review text."""
    prompt = f"""
Extract the following into JSON.
Review: {review_text}
Return a JSON array of objects like:
{{"category": " ", "value": " ", "sentiment": 1}}
Use only categories from this list: {category_text}
"""
    response = ask_gemini(prompt)
    response = _clean_json_response(response)
    return json.loads(response)
