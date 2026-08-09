"""LLM and embedding integration for the drama companion app."""

import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment.")

# Gemini text generation client.
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)

# Raw Gemini client for structured output and direct content generation.
client = genai.Client(api_key=GEMINI_API_KEY)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def get_client():
    """Return the underlying Gemini client."""
    return client


def ask_gemini(prompt: str) -> str:
    """Return a Gemini text completion from the raw Gemini client."""
    response = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
    return response.text


def get_embedding(text: str) -> list:
    """Return an embedding vector for the given text."""
    return embeddings_model.embed_query(text)
