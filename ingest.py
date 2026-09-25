import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCS_DIR = "./docs"
VECTOR_DB_DIR = "./vector_db"

def build_vector_store():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Created '{DOCS_DIR}' directory. Place your .pdf or .txt files inside it.")
        return

    documents = []

    # 1. Load PDF files if present
    pdf_loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents.extend(pdf_loader.load())

    # 2. Load TXT files directly
    for file in os.listdir(DOCS_DIR):
        if file.endswith(".txt"):
            file_path = os.path.join(DOCS_DIR, file)
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    if not documents:
        print("No .pdf or .txt documents found in 'docs/'. Add files and re-run.")
        return

    print(f"Loaded {len(documents)} document(s). Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("Generating local embeddings (Free, HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Persist chunks to ChromaDB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )
    print("RAG Knowledge Base successfully created and persisted to 'vector_db/'!")

if __name__ == "__main__":
    build_vector_store()