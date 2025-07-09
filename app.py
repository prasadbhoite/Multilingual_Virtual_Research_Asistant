import streamlit as st
from utils.llama_client import (
    ask_question,
    summarize_text,
    analyze_image_url,
    multilingual_translate,
)

st.set_page_config(page_title="MVRA - Assistant", layout="wide")

# Step 1: API Credential Input
display_api_prompt = "api_key" not in st.session_state or "base_url" not in st.session_state
if display_api_prompt:
    st.title("🔐 Enter LLaMA API Credentials")

    api_key = st.text_input("LLaMA API Key", type="password")
    base_url = st.text_input("LLaMA Base URL", placeholder="https://api.llama.com/v1")

    if st.button("Continue"):
        if api_key and base_url:
            st.session_state.api_key = api_key
            st.session_state.base_url = base_url
            st.rerun()
        else:
            st.error("Please enter both API key and base URL.")
    st.stop()

# Step 2: Main App UI
st.title("🧠 MVRA: Assistant")

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Ask a Question", 
    "📰 Summarize Text", 
    "🖼️ Analyze Image (URL)", 
    "🌍 Multilingual Translator"
])

with tab1:
    st.subheader("Ask any question")
    question = st.text_area("Enter your question", height=150)
    if st.button("Get Answer", key="qa"):
        with st.spinner("Thinking..."):
            if question:
                answer = ask_question(question, st.session_state.api_key, st.session_state.base_url)
                st.success("Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question.")

with tab2:
    st.subheader("Summarize a long text")
    text_input = st.text_area("Paste text to summarize", height=300)
    if st.button("Summarize", key="sum"):
        with st.spinner("Summarizing..."):
            if text_input:
                summary = summarize_text(text_input, st.session_state.api_key, st.session_state.base_url)
                st.success("Summary:")
                st.write(summary)
            else:
                st.warning("Please enter some text.")

with tab3:
    st.subheader("Analyze image from URL")
    prompt = st.text_input("What would you like to know about the image?")
    image_url = st.text_input("Enter a valid image URL")
    if st.button("Analyze Image"):
        if not image_url or not prompt:
            st.warning("Please provide both an image URL and a prompt.")
        else:
            st.image(image_url, caption="Image Preview", use_container_width=True)
            with st.spinner("Analyzing image..."):
                result = analyze_image_url(prompt, image_url, st.session_state.api_key)
                st.success("Result:")
                st.write(result)

with tab4:
    st.subheader("Multilingual Translation Chat")
    user_input = st.text_area("Enter your message")
    source_lang = st.selectbox("Source Language", ["English", "French", "Spanish", "Hindi", "Chinese"])
    target_lang = st.selectbox("Target Language", ["English", "French", "Spanish", "Hindi", "Chinese"])
    if st.button("Translate"):
        if not user_input:
            st.warning("Please enter a message.")
        else:
            with st.spinner("Translating..."):
                result = multilingual_translate(
                    message=user_input,
                    source=source_lang,
                    target=target_lang,
                    api_key=st.session_state.api_key,
                    base_url="https://api.llama.com/compat/v1/"
                )
                st.success("Translation Result:")
                st.write(result)
