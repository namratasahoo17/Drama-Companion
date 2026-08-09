from enum import Enum
from pydantic import BaseModel

class Intent(str, Enum):
    CHAT = "chat"
    REVIEW = "review"
    RECOMMENDATION = "recommendation"
    QUESTION = "question"

class RouterOutput(BaseModel):
    intent: Intent
    drama_title: str | None = None

