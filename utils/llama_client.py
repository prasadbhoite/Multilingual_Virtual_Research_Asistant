import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LLAMA_API_KEY}"
}


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

def extract_response_content(response: dict) -> str:
    try:
        message = response.get("completion_message")
        content = message["content"]["text"] if isinstance(message["content"], dict) else message["content"]
        return content.strip()
    except Exception as e:
        return f"[Error extracting content: {e}]"
