import os
import json
import datetime
import webbrowser
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
from groq import Groq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
VECTOR_DB_DIR = "./vector_db"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def say(text: str):
    """Prints and speaks the assistant's response."""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def search_rag_database(query: str) -> str:
    """Searches the local ChromaDB vector database using local embeddings."""
    if not os.path.exists(VECTOR_DB_DIR):
        return "RAG database is empty. Please add files to docs/ and run ingest.py first."
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    results = vector_db.similarity_search(query, k=3)
    
    if not results:
        return "No relevant context found in local knowledge base."
    
    context = "\n---\n".join([doc.page_content for doc in results])
    return f"Retrieved Context:\n{context}"

# Function definitions for Groq tool calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Opens a requested website or URL in the default web browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL or domain to open (e.g., youtube.com)"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current local time.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_knowledge_base",
            "description": "Searches the user's local document knowledge base (RAG).",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {"type": "string", "description": "Topic or query to search"}
                },
                "required": ["search_query"]
            }
        }
    }
]

def execute_tool(func_name, args):
    """Executes local functions based on model tool selection."""
    if func_name == "open_website":
        url = args.get("url")
        if not url.startswith("http"):
            url = f"https://www.{url}"
        webbrowser.open(url)
        return f"Successfully opened {url}"

    elif func_name == "get_current_time":
        return datetime.datetime.now().strftime("The current time is %I:%M %p")

    elif func_name == "query_knowledge_base":
        return search_rag_database(args.get("search_query"))

    return "Unknown tool called."

def listen():
    """Captures microphone input and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 0.8
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            print(f"User: {query}")
            return query
        except sr.WaitTimeoutError:
            return ""
        except Exception:
            return ""

def chat(messages):
    """Handles interaction with Groq model and function execution."""
    # Active model directly from your Groq key model list
    model_id = "openai/gpt-oss-20b"

    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            tool_output = execute_tool(func_name, args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })
        
        final_response = client.chat.completions.create(
            model=model_id,
            messages=messages
        )
        return final_response.choices[0].message.content

    return msg.content

if __name__ == "__main__":
    say("Jarvis AI system online and operational.")
    conversation = [
        {
            "role": "system",
            "content": "You are Jarvis, a concise and intelligent AI voice assistant equipped with RAG capabilities."
        }
    ]

    while True:
        user_input = listen()
        if not user_input:
            continue

        if any(word in user_input.lower() for word in ["quit", "exit", "stop"]):
            say("Deactivating systems. Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})
        reply = chat(conversation)
        conversation.append({"role": "assistant", "content": reply})
        say(reply)