import streamlit as st
from core.graph import graph
from database import engine
from models import Base

# Ensure database tables exist before the UI loads.
Base.metadata.create_all(engine)

st.set_page_config(
    page_title="Drama Companion",
    page_icon="??",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 47%, #1f3b6f 100%);
        color: #f8fafc;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.15);
        color: #f8fafc;
    }
    .chat-box {
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.17);
    }
    .user-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.16);
    }
    .assistant-box {
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.22);
    }
    .message-role {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .message-text {
        font-size: 1rem;
        line-height: 1.7;
        color: #f8fafc;
    }
    .metadata-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "drama" not in st.session_state:
    st.session_state.drama = None
if "intent" not in st.session_state:
    st.session_state.intent = None

st.title("?? Drama Companion")
st.markdown("A friendly UI for chatting with your drama companion chatbot.")

with st.expander("How it works", expanded=False):
    st.write(
        "This UI sends your message into the existing drama companion backend, "
        "classifies intent, loads drama context, and replies conversationally. "
        "If you share a review, it also extracts structured preferences."
    )

left, right = st.columns([3, 1])

with left:
    user_input = st.text_area(
        "Your message",
        placeholder="Tell me about a drama, ask for a recommendation, or write a review...",
        key="input_message",
        height=170,
    )

    if st.button("Send"):
        prompt_text = user_input.strip()
        if prompt_text:
            state = {
                "user_input": prompt_text,
                "recent_messages": st.session_state.conversation[-6:],
            }
            result = graph.invoke(state)

            st.session_state.conversation.append({"role": "user", "message": prompt_text})
            st.session_state.conversation.append({"role": "assistant", "message": result.get("response", "")})
            st.session_state.intent = result.get("intent")
            st.session_state.drama = result.get("drama")
            st.session_state.input_message = ""
        else:
            st.warning("Please enter a message before sending.")

    if st.button("Clear conversation"):
        st.session_state.conversation = []
        st.session_state.intent = None
        st.session_state.drama = None

    st.markdown("---")
    st.subheader("Conversation")

    if not st.session_state.conversation:
        st.info("Start chatting to see your drama companion in action.")
    else:
        for message in st.session_state.conversation:
            role = message["role"]
            text = message["message"]
            box_class = "assistant-box" if role == "assistant" else "user-box"
            st.markdown(
                f"<div class='chat-box {box_class}'>"
                f"<div class='message-role'>{role.capitalize()}</div>"
                f"<div class='message-text'>{text}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

with right:
    st.subheader("Session info")
    st.markdown("---")
    st.write("**Intent:**", st.session_state.intent or "not classified yet")
    st.write("**Drama:**", st.session_state.drama["title"] if st.session_state.drama else "none")

    if st.session_state.drama:
        st.markdown("<div class='metadata-card'>", unsafe_allow_html=True)
        st.write("**Synopsis**")
        st.write(st.session_state.drama.get("synopsis", "N/A"))
        st.write("**Genres**", st.session_state.drama.get("genres", "N/A"))
        st.write("**Episodes**", st.session_state.drama.get("episodes", "N/A"))
        st.write("**Network**", st.session_state.drama.get("network", "N/A"))
        st.write("**Release year**", st.session_state.drama.get("release_year", "N/A"))
        st.write("**Country**", st.session_state.drama.get("country", "N/A"))
        st.write("**Aspects**")
        aspects = st.session_state.drama.get("aspects", [])
        if aspects:
            for aspect in aspects:
                st.write(f"- **{aspect['name'].capitalize()}**: {aspect['score']}/10 — {aspect['reason']}")
        else:
            st.write("No extracted drama aspects yet.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='margin-top: 30px; color: #cbd5e1;'>"
    "Built with Python and Streamlit. Run `streamlit run ui/streamlit_app.py` to launch the UI."
    "</div>",
    unsafe_allow_html=True,
)
