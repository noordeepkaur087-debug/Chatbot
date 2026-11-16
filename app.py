import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Knowledge-Based Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Gemini Knowledge-Based Chatbot")
st.caption("Ask questions based on the knowledge/manual you provide.")

# Load the API key securely from Streamlit secrets or an environment variable.
api_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
api_key = api_key or os.getenv("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("Chatbot settings")
    model_name = st.text_input("Gemini model", value="gemini-2.5-flash")
    manual = st.text_area(
        "Knowledge / Manual",
        value="Paste your knowledge or manual here.",
        height=260,
        help="The chatbot will use this text as its reference material.",
    )
    system_prompt = st.text_area(
        "System instruction",
        value=(
            "You are a helpful knowledge-based chatbot. Answer the user's question "
            "using the provided manual as your primary source. If the answer is not "
            "available in the manual, clearly say that the manual does not contain "
            "that information. Do not invent facts. Keep answers clear and relevant."
        ),
        height=180,
    )
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display earlier messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    if not api_key:
        error_message = (
            "Gemini API key not found. Add `GEMINI_API_KEY` to "
            "`.streamlit/secrets.toml` or set it as an environment variable."
        )
        with st.chat_message("assistant"):
            st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    elif not manual.strip() or manual.strip() == "Paste your knowledge or manual here.":
        error_message = "Please add your knowledge/manual in the sidebar before asking a question."
        with st.chat_message("assistant"):
            st.warning(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = genai.Client(api_key=api_key)

                    # Include the conversation history so follow-up questions have context.
                    conversation = [
                        types.Content(
                            role="user",
                            parts=[types.Part.from_text(
                                text="KNOWLEDGE / MANUAL:\\n" + manual
                            )],
                        )
                    ]
                    for item in st.session_state.messages:
                        role = "user" if item["role"] == "user" else "model"
                        conversation.append(
                            types.Content(
                                role=role,
                                parts=[types.Part.from_text(text=item["content"])],
                            )
                        )

                    response = client.models.generate_content(
                        model=model_name,
                        contents=conversation,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        ),
                    )
                    answer = response.text or "I couldn't generate a text response. Please try again."
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as exc:
                    error_message = f"An error occurred: {exc}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
