from llm import llm
from core.schemas import RouterOutput
from core.state import AppState

structured_llm = llm.with_structured_output(RouterOutput)

def format_history(recent_messages):
    if not recent_messages:
        return "(no prior messages)"
    return "\n".join(f"{m['role']}: {m['message']}" for m in recent_messages)
 
 
def router_node(state: AppState):
    history_text = format_history(state.get("recent_messages"))
 
    prompt = f"""
You are an intent classifier for a drama companion app.
 
Recent conversation (for context — use it to resolve things like "it",
"the ending", or a question about a drama that isn't named again):
{history_text}
 
Classify the CURRENT user message into exactly one of these intents:
 
- CHAT: small talk, greetings, no specific drama opinion
- REVIEW: the user is sharing their own opinion/reaction about a drama they watched
- RECOMMENDATION: the user is asking to be recommended something
- QUESTION: the user is asking the AI something, e.g. asking what IT thinks, or asking for information
 
Also extract the drama title being discussed. If the current message doesn't
name one but the recent conversation makes it clear which drama is meant,
use that title. Otherwise return null.
 
Current user message:
{state["user_input"]}
"""

    result = structured_llm.invoke(prompt)

    return {
        **state,
        "intent": result.intent,
        "drama_title": result.drama_title
    }