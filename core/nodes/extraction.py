from core.state import AppState
from extractor import extract_review, extract_preferences
from services import save_review, save_preferences

CATEGORY_TEXT = "genre,pacing,trope,actor,ending_style"

def extraction_node(state: AppState) -> AppState:
    review_text = state["user_input"]

    data = extract_review(review_text)

    drama_id = state["drama"]["id"] if state.get("drama") else None
    save_review(data, drama_id=drama_id)

    prefs = extract_preferences(review_text, CATEGORY_TEXT)
    save_preferences(prefs, drama_id=drama_id)
    return state