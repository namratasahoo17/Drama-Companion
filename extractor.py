"""Text extraction utilities for reviews and user preferences."""

import json
import re

from llm import ask_gemini


def _clean_json_response(response: str) -> str:
    """Remove Markdown fences and surrounding whitespace."""
    cleaned = response.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_json(response: str, expected_type):
    """Parse model JSON and raise a clear error for invalid output."""
    cleaned = _clean_json_response(response)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini returned invalid JSON: {cleaned}") from exc

    if not isinstance(data, expected_type):
        raise ValueError(
            f"Gemini returned {type(data).__name__}; "
            f"expected {expected_type.__name__}."
        )
    return data


def extract_review(review_text: str) -> dict:
    """Extract a structured review object from free-form text."""
    prompt = f"""
Extract the user's drama review into JSON.

Review:
{review_text}

Return only valid JSON matching:
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

Use a numeric rating from 0 to 10. If an aspect is not mentioned,
do not invent one.
"""
    return _parse_json(ask_gemini(prompt), dict)


def extract_preferences(review_text: str, category_text: str) -> list:
    """Extract preference records from review text."""
    prompt = f"""
Extract only preferences clearly expressed by the user.

Review:
{review_text}

Return a JSON array of objects:
{{"category": "", "value": "", "sentiment": 1}}

Allowed categories: {category_text}
Sentiment must be between -1 and 1.
Return [] if no preference is clear.
"""
    return _parse_json(ask_gemini(prompt), list)
