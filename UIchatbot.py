import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #4CAF50;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="title">🤖 AI Personality Chatbot</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Chat with Angry, Funny, or Sad AI</div>',
    unsafe_allow_html=True
)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("⚙️ Settings")

personality = st.sidebar.radio(
    "Choose AI Personality",
    ["😡 Angry", "😂 Funny", "😢 Sad"]
)

if personality == "😡 Angry":
    mode = """
    You are an angry AI assistant.
    Respond aggressively, impatiently,
    and slightly sarcastically.
    """

elif personality == "😂 Funny":
    mode = """
    You are a funny AI assistant.
    Respond with humor, jokes,
    and light-hearted comments.
    """

else:
    mode = """
    You are a sad AI assistant.
    Respond in a gloomy,
    emotional, and sad tone.
    """

# ----------------------------
# Clear Chat Button
# ----------------------------
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]
    st.rerun()

# ----------------------------
# Model
# ----------------------------
model = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.9,
    max_tokens=100
)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# Update system prompt if mode changes
st.session_state.messages[0] = SystemMessage(content=mode)

# ----------------------------
# Display Chat History
# ----------------------------
for msg in st.session_state.messages[1:]:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

            st.markdown(response.content)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )