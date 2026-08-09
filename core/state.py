from typing import TypedDict
from core.schemas import Intent

class AppState(TypedDict):
    user_input: str
    intent: Intent | None
    drama_title: str | None
    drama: dict | None
    response: str |None
    recent_messages: list