import streamlit as st
from google import genai
from google.genai import types
import os

st.set_page_config(page_title="Swamp Tutor", page_icon="🐊")
st.title("🐊 Swamp Tutor")
st.caption("Step-by-step help for UF & SF students. No direct answers, just pure learning.")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

tutor_config = types.GenerateContentConfig(
    system_instruction=(
        "You are an expert AI tutor for university students. "
        "Never give the direct answer to homework or code problems. "
        "Explain concepts step-by-step and ask guiding questions to help the user arrive at the answer."
    ),
    temperature=0.3
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=tutor_config
    )
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("E.g., I don't understand MAC2311 derivatives..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
