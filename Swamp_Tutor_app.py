import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Swamp Tutor", page_icon="🐊")
st.title("🐊 Swamp Tutor")
st.caption("Step-by-step help for UF & SF students. No direct answers, just pure learning.")

# 1. ALWAYS initialize a fresh client on every run so the connection never closes
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tutor_config = types.GenerateContentConfig(
    system_instruction=(
        "You are an expert AI tutor for university students. "
        "Never give the direct answer to homework or code problems. "
        "Explain concepts step-by-step and ask guiding questions to help the user arrive at the answer."
    ),
    temperature=0.3
)

# 2. Rely entirely on Streamlit to remember the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("E.g., I don't understand MAC2311 derivatives..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Convert Streamlit's saved history into the exact format Google expects
    api_contents = []
    for msg in st.session_state.messages:
        # Google requires the assistant role to be strictly named "model"
        api_role = "model" if msg["role"] == "assistant" else "user"
        api_contents.append(
            types.Content(
                role=api_role, 
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    # 4. Generate the response cleanly without relying on a stateful session
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-1.5-flash-8b",
            contents=api_contents,
            config=tutor_config
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
