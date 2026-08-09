"""Command-line entrypoint for the drama companion chatbot."""

from core.graph import graph
from database import engine
from models import Base


def run(message: str, recent_messages: list) -> dict:
    """Invoke the workflow graph with the current user input and recent history."""
    result = graph.invoke(
        {
            "user_input": message,
            "recent_messages": recent_messages,
        }
    )
    print("response:", result.get("response"))
    print()
    return result


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session_history = []
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break

        result = run(message, session_history[-6:])
        session_history.append({"role": "user", "message": message})
        session_history.append({"role": "assistant", "message": result.get("response")})
