
# 🧠 MVRA: Multilingual Virtual Research Assistant

MVRA is a modular, Streamlit-based AI assistant powered by LLaMA 4 API. This lightweight app supports interactive **text question answering** and **text summarization**, with planned support for multimodal capabilities including images, tables, and multilingual inputs.

---

## 🚀 Features

- 🔍 **Ask questions** on any topic using LLaMA 4 models.
- 📰 **Summarize long texts** into concise insights.
- 🔐 **Secure session-based API configuration** (no API keys in code).
- 📦 **Modular structure** for easy extension (PDFs, images, etc.).
- 💬 **Coming soon**: Image Q&A, multilingual input, code from screenshot, and more.

---

## 🛠️ Project Structure

```
mvra_app/
│
├── app.py                  # Streamlit app with text-based features
├── requirements.txt        # Python dependencies
├── .env (optional)         # Store local API keys (not committed)
│
├── utils/
│   ├── llama_client.py     # Handles LLaMA 4 chat completions
│
└── README.md               # You're here!
```

---

## ⚙️ Getting Started

### 1. 📥 Clone the Repo

```bash
git clone https://github.com/your-username/mvra_app.git
cd mvra_app
```

### 2. 🐍 Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔑 Run the App

```bash
streamlit run app.py
```

You will be prompted to enter your:
- **LLaMA 4 API Key**
- **LLaMA 4 Base URL** (e.g., `https://api.llama.meta.com/v1`)

These credentials are stored in `st.session_state` for the duration of the session.

---

## 🧪 Example Models

- `Llama-3.3-8B-Instruct`
- `Llama-4-8B-Instruct`
- `Llama-4-Scout-17B-16E-Instruct-FP8`

---

## 📌 Notes

- No API keys are hardcoded — safe for open-source or demos.
- You can modify `utils/llama_client.py` to support streaming or model selection.
- Future enhancements may include:
  - PDF summarization
  - Image Q&A and grounding
  - Code generation from screenshots
  - Multilingual text and voice support

---

## 🧠 Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [Meta LLaMA API](https://ai.meta.com/llama/)
- [Python](https://python.org)

---

## 📄 License

MIT License © 2025 [Prasad Bhoite]
