"""Post-response extraction for reviews and preferences."""

from core.state import AppState
from extractor import extract_preferences, extract_review
from services import save_preferences, save_review

CATEGORY_TEXT = "genre,pacing,trope,actor,ending_style"


def extraction_node(state: AppState) -> AppState:
    """Extract and persist review data without breaking the chatbot reply."""
    review_text = state["user_input"]
    drama = state.get("drama") or {}

    try:
        data = extract_review(review_text)

        # Use the title already identified by the graph when extraction omits it.
        if not data.get("title") and drama.get("title"):
            data["title"] = drama["title"]

        if data.get("title") or drama.get("id"):
            save_review(data, drama_id=drama.get("id"))

        prefs = extract_preferences(review_text, CATEGORY_TEXT)
        save_preferences(prefs, drama_id=drama.get("id"))
    except Exception as exc:
        # A review-extraction failure must not discard a successful chat reply.
        return {**state, "extraction_error": str(exc)}

    return state
