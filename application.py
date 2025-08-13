import streamlit as st
from assistant import Assistant

st.set_page_config(page_title="Personal AI", page_icon="🤖", layout="centered")
st.title("🤖 Your Personal AI Assistant")

if "assistant" not in st.session_state:
    st.session_state.assistant = Assistant()
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Ask me anything...")

if st.button("Send") and user_input:
    response = st.session_state.assistant.chat(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("AI", response))

for role, text in st.session_state.history:
    if role == "You":
        st.markdown(f"**🧍 {role}:** {text}")
    else:
        st.markdown(f"**🤖 {role}:** {text}")

