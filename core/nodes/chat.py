from core.state import AppState
from core.schemas import Intent
from llm import ask_gemini
from services import save_conversation


def format_history(recent_messages):
    if not recent_messages:
        return "(this is the start of the conversation)"
    return "\n".join(f"{m['role']}: {m['message']}" for m in recent_messages)


def chat_node(state: AppState):
    intent = state.get("intent")
    drama = state.get("drama")
    user_input = state["user_input"]
    history_text = format_history(state.get("recent_messages"))

    needs_drama = intent in (Intent.REVIEW, Intent.RECOMMENDATION)

    if needs_drama and not drama:
        response = "I don't think I know that drama yet — tell me a bit about it?"

    elif drama:
        aspects_text = ""
        for i in drama["aspects"]:
            aspects_text += i["name"] + ": " + str(i["score"]) + "/10 (" + i["reason"] + ")\n"

        prompt = f"""You are a warm, casual drama companion chatbot talking to a
friend about the drama "{drama['title']}".

Recent conversation:
{history_text}

What the user has said about this drama before:
{aspects_text}

The user just said: "{user_input}"

Reply naturally and conversationally, like a friend who knows this drama
and remembers what was just said. Keep it short (1-3 sentences)."""
        response = ask_gemini(prompt)

    else:
        prompt = f"""You are a warm, casual drama companion chatbot talking to a
friend about the drama "{drama['title']}".

Recent conversation:
{history_text}

What the user has said about this drama before:
{aspects_text}

The user just said: "{user_input}"

Reply naturally and conversationally, like a friend who remembers what was
just said. Don't restate or announce who/what you think they're referring
to — just respond as if it's obvious, the way a real friend would.
Keep it short (1-3 sentences)."""
        response = ask_gemini(prompt)

    drama_id = drama["id"] if drama else None
    save_conversation("user", user_input, drama_id=drama_id)
    save_conversation("assistant", response, drama_id=drama_id)

    return {
        **state,
        "response": response,
    }