import streamlit as st
from utils.llama_client import (
    ask_question,
    summarize_text,
    analyze_image_url,
    analyze_multiple_images,
    multilingual_translate,
    analyze_uploaded_image,
    analyze_uploaded_multiple_images,
    analyze_image_grounding,
    parse_output,
    draw_bounding_boxes_from_bytes,
)

st.set_page_config(page_title="MVRA - Assistant", layout="wide")

# Step 1: API Credential Input
if "api_key" not in st.session_state or "base_url" not in st.session_state:
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

# Main UI
st.title("🧠 MVRA: Assistant")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📝 Ask a Question",
    "📰 Summarize Text",
    "🖼️ Analyze Single Image (URL)",
    "🖼️ Analyze Multiple Images (URL)",
    "🌍 Multilingual Translator",
    "📤 Analyze Uploaded Image",
    "📤 Analyze Multiple Uploaded Images",
    "📍 Image Grounding" 
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
    st.subheader("Analyze a single image from URL")
    prompt = st.text_input("What would you like to know about the image?", placeholder="What's in the image?")
    image_url = st.text_input("Enter a valid image URL", placeholder= "https://raw.githubusercontent.com/meta-llama/llama-models/refs/heads/main/Llama_Repo.jpeg")
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
    st.subheader("Analyze multiple images (max 9)")
    prompt = st.text_input("What would you like to know about these images?", placeholder="Compare the following images?")
    urls_input = st.text_area("Paste up to 9 image URLs (one per line)", 
    placeholder= """https://raw.githubusercontent.com/meta-llama/llama-models/refs/heads/main/Llama_Repo.jpeg
    https://raw.githubusercontent.com/meta-llama/PurpleLlama/refs/heads/main/logo.png""")
    image_urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    if st.button("Analyze Multiple Images"):
        if not prompt or not image_urls:
            st.warning("Please provide a prompt and at least one image URL.")
        elif len(image_urls) > 9:
            st.warning("You can only analyze up to 9 images.")
        else:
            for img_url in image_urls:
                st.image(img_url, caption=img_url, use_container_width=True)
            with st.spinner("Analyzing multiple images..."):
                result = analyze_multiple_images(prompt, image_urls, st.session_state.api_key)
                st.success("Result:")
                st.write(result)

with tab5:
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

with tab6:
    st.subheader("Analyze a single uploaded image")
    prompt = st.text_input("What would you like to ask about the uploaded image?")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("Analyze Uploaded Image"):
        if not uploaded_file or not prompt:
            st.warning("Please upload an image and enter a prompt.")
        else:
            image_bytes = uploaded_file.read()
            st.image(image_bytes, caption="Uploaded Image", use_container_width=True)
            with st.spinner("Analyzing uploaded image..."):
                result = analyze_uploaded_image(
                    prompt=prompt,
                    image_bytes=image_bytes,
                    api_key=st.session_state.api_key
                )
                st.success("Analysis Result:")
                st.write(result)

with tab7:
    st.subheader("Analyze multiple uploaded images (up to 9)")
    prompt = st.text_input("What would you like to ask about these images?")
    uploaded_files = st.file_uploader(
        "Upload up to 9 images", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if st.button("Analyze Uploaded Images"):
        if not uploaded_files or not prompt:
            st.warning("Please upload images and enter a prompt.")
        elif len(uploaded_files) > 9:
            st.warning("You can only analyze up to 9 images.")
        else:
            for img in uploaded_files:
                st.image(img, caption=img.name, use_container_width=True)

            with st.spinner("Analyzing uploaded images..."):
                result = analyze_uploaded_multiple_images(
                    prompt=prompt,
                    image_files=uploaded_files,
                    api_key=st.session_state.api_key
                )
                st.success("Analysis Result:")
                st.write(result)



with tab8:
    st.subheader("🧠 Image Grounding")
    grounding_prompt = st.text_input("Enter your prompt for image grounding", value="Which tools in the image can be used for measuring length?")
    uploaded_grounding_image = st.file_uploader("Upload an image for grounding", type=["jpg", "jpeg", "png"], key="grounding")

    if st.button("Run Grounding"):
        if not uploaded_grounding_image or not grounding_prompt:
            st.warning("Please provide both an image and a prompt.")
        else:
            image_bytes = uploaded_grounding_image.read()
            st.image(image_bytes, caption="Uploaded Image", use_container_width=True)
            with st.spinner("Grounding image..."):
                response = analyze_image_grounding(
                    prompt=grounding_prompt,
                    image_bytes=image_bytes,
                    api_key=st.session_state.api_key
                )
                tools = parse_output(response)
                st.success("Grounding Result:")
                draw_bounding_boxes_from_bytes(image_bytes, tools)
                st.code(response)
