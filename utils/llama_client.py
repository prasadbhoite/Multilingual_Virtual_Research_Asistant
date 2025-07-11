## utils/llama_client.py
import os
import requests
from llama_api_client import LlamaAPIClient
from openai import OpenAI

def chat_completion(messages, api_key, base_url, model="Llama-3.3-8B-Instruct", max_tokens=256):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "messages": messages,
        "model": model,
        "max_tokens": max_tokens,
        "stream": False
    }

    response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json()

def ask_question(question: str, api_key: str, base_url: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides concise answers."},
        {"role": "user", "content": question}
    ]
    response = chat_completion(messages, api_key, base_url)
    return extract_response_content(response)

def summarize_text(text: str, api_key: str, base_url: str) -> str:
    messages = [
        {"role": "system", "content": "You are a summarization assistant. Create concise summaries that capture the key points of the provided text."},
        {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
    ]
    response = chat_completion(messages, api_key, base_url, max_tokens=150)
    return extract_response_content(response)

def analyze_image_url(prompt: str, image_url: str, api_key: str,
                      model="Llama-4-Scout-17B-16E-Instruct-FP8") -> str:
    content = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": image_url}}
    ]
    client = LlamaAPIClient(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=0
    )
    return response.completion_message.content.text

def analyze_multiple_images(prompt: str, image_urls: list, api_key: str,
                            model="Llama-4-Scout-17B-16E-Instruct-FP8") -> str:
    if not image_urls:
        return "No image URLs provided."
    if len(image_urls) > 9:
        return "You can only analyze up to 9 images."

    content = [{"type": "text", "text": prompt}]
    content.extend([{"type": "image_url", "image_url": {"url": url}} for url in image_urls])

    client = LlamaAPIClient(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=0
    )
    return response.completion_message.content.text

def multilingual_translate(message: str, source: str, target: str, api_key: str, base_url: str,
                           model="Llama-4-Scout-17B-16E-Instruct-FP8") -> str:
    client = OpenAI(api_key=api_key, base_url=base_url)
    system_prompt = f"""You're a bilingual translator between two people:
      - The first person only speaks {source}
      - The second person only speaks {target}
Return:
1. Recognized language: <detected language>
2. Translation of the input: <translation>
3. Answer to the input: <in the same language as the detected language>"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def extract_response_content(response: dict) -> str:
    try:
        message = response.get("completion_message")
        content = message["content"]["text"] if isinstance(message["content"], dict) else message["content"]
        return content.strip()
    except Exception as e:
        return f"[Error extracting content: {e}]"
