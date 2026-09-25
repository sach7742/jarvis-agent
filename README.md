# Jarvis AI: Voice Assistant with RAG Agent System

An intelligent, voice-enabled assistant powered by OpenAI Function Calling and ChromaDB for local Retrieval-Augmented Generation (RAG).

## Features
- **Voice Recognition & Speech Output:** Interactive hands-free speech input and output.
- **RAG Architecture:** Query local PDFs and Markdown files via ChromaDB vector retrieval.
- **OpenAI Tool Calling:** Dynamic execution of browser controls, real-time utilities, and RAG search.

## Setup Instructions

1. **Clone Repository:**
   ```bash
   git clone [https://github.com/sach7742/jarvis-rag-agent.git](https://github.com/sach7742/jarvis-rag-agent.git)
   cd jarvis-rag-agent

   Environment & Dependencies:
   python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Configure API Keys:
Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_api_key