
import streamlit as st
from chatbot import FAQChatbot, load_faqs

st.set_page_config(
    page_title="ShopAssist",
    page_icon="🛍️",
    layout="centered",
)

@st.cache_resource
def get_chatbot():
    faqs = load_faqs("data/faqs.json")
    return FAQChatbot(faqs, threshold=0.22)

chatbot = get_chatbot()

st.title("🛍️ ShopAssist")
st.caption("Your online shopping FAQ assistant")

st.write(
    "Hi! 👋 Ask me about orders, payments, delivery, "
    "returns, refunds, and other shopping-related questions."
)

with st.sidebar:
    st.header("About ShopAssist")
    st.write(
        "ShopAssist uses NLP to find relevant answers "
        "from a collection of frequently asked questions."
    )
    st.metric("FAQs available", len(chatbot.faqs))

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Built with Python, NLTK, Scikit-learn and Streamlit")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask about orders, payments, delivery, or returns..."
)

if prompt is not None:
    prompt = prompt.strip()

    if not prompt:
        st.warning("Please enter a question before sending.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        result = chatbot.get_answer(prompt)

        with st.chat_message("assistant"):
            st.markdown(result["answer"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
        })
