"""Command-line entry point for Drama Companion."""

from core.graph import graph
from database import engine
from models import Base


def run(message: str, recent_messages: list) -> dict:
    """Run one message through the LangGraph workflow."""
    return graph.invoke(
        {
            "user_input": message,
            "recent_messages": recent_messages,
        }
    )


def main() -> None:
    """Start the interactive terminal chatbot."""
    Base.metadata.create_all(engine)

    print("=" * 50)
    print("Drama Companion")
    print("Type 'exit' or 'quit' to close.")
    print("=" * 50)

    session_history = []

    while True:
        try:
            message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not message:
            continue

        if message.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            result = run(message, session_history[-6:])
            response = result.get("response") or "I couldn't generate a response."
            print(f"\nAssistant: {response}")

            session_history.extend(
                [
                    {"role": "user", "message": message},
                    {"role": "assistant", "message": response},
                ]
            )

            if result.get("extraction_error"):
                print(
                    "\n[Note: the reply worked, but review extraction "
                    "could not be saved this time.]"
                )
        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
