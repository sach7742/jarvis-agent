# 🤖 Jarvis Voice Agent: Voice AI Assistant with Local RAG

A lightweight, high-performance voice assistant powered by **Groq Function Calling**, **LangChain**, and **ChromaDB**. 

Jarvis handles real-time voice interactions, opens applications/websites, retrieves local time, and executes **Retrieval-Augmented Generation (RAG)** over custom local documents (`.pdf` and `.txt`) using local vector embeddings.

---

## 📸 Key Features

- **⚡ Fast Voice-to-Voice Inference:** Uses Groq's low-latency LLM engine combined with Google Speech Recognition and `pyttsx3` text-to-speech.
- **📚 Local Document RAG:** Uses HuggingFace sentence-transformers (`all-MiniLM-L6-v2`) and ChromaDB vector store to query documents locally—no sensitive data leaves your machine.
- **🛠️ Dynamic Function Calling:** Seamlessly routes user intents to local Python tools (Browser navigation, System Time, Vector Search).
- **💰 100% Free & Open-Source:** Built completely on free-tier APIs and local open-weight models.

---

## 🏗️ Architecture

```text
               ┌───────────────────────┐
               │    Voice Input (Mic)  │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │   Google Speech STT   │
               └───────────┬───────────┘
                           │
                           ▼
               ┌───────────────────────┐
               │     Groq LLM Engine   │ ◄── [Tool Dispatching]
               └───────────┬───────────┘
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ open_website │  │ get_curr_time│  │ RAG Query DB │
  └──────────────┘  └──────────────┘  └──────┬───────┘
                                             │
                                             ▼
                                      ┌──────────────┐
                                      │   ChromaDB   │
                                      │ (HuggingFace │
                                      │  Embeddings) │
                                      └──────────────┘

```

---

## 🚀 Quickstart Guide

### 1. Prerequisites

* **Python:** `3.10` or higher
* **System Dependencies (macOS):**
```bash
brew install portaudio

```



### 2. Environment Setup

Clone the repository and activate a Python virtual environment:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/jarvis-agent.git](https://github.com/YOUR_GITHUB_USERNAME/jarvis-agent.git)
cd jarvis-agent

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

```

### 3. API Key Configuration

Create a `.env` file in the root directory and add your free **Groq API Key** (obtainable from [Groq Console](https://console.groq.com/?utm_source=gemini)):

```env
GROQ_API_KEY=gsk_your_groq_api_key_here

```

---

## 📖 Usage Instructions

### 1. Ingest Documents into RAG Vector Store

1. Place your target `.pdf` or `.txt` files inside the `docs/` folder.
2. Build the local vector database:

```bash
python ingest.py

```

### 2. Start Jarvis Voice Assistant

Run the main assistant script:

```bash
python main.py

```

---

## 💬 Sample Voice Commands

* **General Queries:** *"What time is it?"*
* **Browser Control:** *"Open YouTube"*, *"Open GitHub"*
* **RAG Document Search:** *"Jarvis, query my knowledge base for..."*, *"What does my study guide say about pointer memory?"*
* **Exit System:** *"Stop Jarvis"*, *"Quit"*, *"Exit"*

---

## 🛠️ Project Structure

```text
jarvis-agent/
│── docs/               # Local document storage (.pdf / .txt)
│── vector_db/          # Persistent ChromaDB store (auto-generated)
│── .env                # API Credentials (Excluded from Git)
│── .gitignore          # Excluded directories
│── requirements.txt    # Project dependencies
│── ingest.py           # Document chunking & embedding pipeline
│── main.py             # Voice recognition & LLM orchestrator
└── README.md           # Documentation

```

---

