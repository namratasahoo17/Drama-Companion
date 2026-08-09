"""Gemini integration used by the LangGraph workflow."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")


def _require_api_key() -> str:
    """Return the API key or explain exactly how to configure it."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Create a .env file in the project folder "
            "and add: GEMINI_API_KEY=your_key"
        )
    return key


@lru_cache(maxsize=1)
def get_client():
    """Return the native Gemini client."""
    return genai.Client(api_key=_require_api_key())


@lru_cache(maxsize=1)
def get_llm():
    """Return the LangChain Gemini model used by the router."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=_require_api_key(),
        temperature=0,
    )


class _LazyLLM:
    """Preserve the original ``llm.with_structured_output`` API."""

    def with_structured_output(self, schema):
        return get_llm().with_structured_output(schema)


llm = _LazyLLM()


def ask_gemini(prompt: str) -> str:
    """Generate a text response with Gemini."""
    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
