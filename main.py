from core.graph import graph
from database import engine
from models import Base


def run(message, recent_messages):
    result = graph.invoke({
        "user_input": message,
        "recent_messages": recent_messages,
    })

    print("response:    ", result.get("response"))
    print()

    return result


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    session_history = []  # list of {"role": ..., "message": ...}, this session only

    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break

        # only send the last few turns — keeps the prompt small
        result = run(message, session_history[-6:])

        session_history.append({"role": "user", "message": message})
        session_history.append({"role": "assistant", "message": result.get("response")})