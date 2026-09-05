"""
End-to-End LangChain RAG Application
====================================

Loads every PDF from a folder, splits them into chunks, embeds the chunks
into a Chroma vector store, and answers questions using Google Gemini with
the retrieved context (Retrieval-Augmented Generation).

Pipeline:
    PDF folder  ->  DirectoryLoader + PyMuPDF4LLMLoader   (load)
                ->  RecursiveCharacterTextSplitter         (chunk)
                ->  GoogleGenerativeAIEmbeddings           (embed)
                ->  Chroma (persisted on disk)             (store / retrieve)
                ->  ChatGoogleGenerativeAI                 (generate answer)

Install (matches the rest of this project's notebooks):
    pip install langchain langchain-community langchain-core langchain-chroma \
                langchain-text-splitters langchain-google-genai \
                langchain-pymupdf4llm chromadb python-dotenv

Run:
    python rag_pdf_app.py                      # interactive Q&A
    python rag_pdf_app.py "your question?"     # single question, then exit
    python rag_pdf_app.py --rebuild            # force re-index of the PDFs
"""

import os
import sys
import argparse

from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder that holds the source PDFs (this project keeps sample books here).
PDF_FOLDER = os.path.join(BASE_DIR, "DocumentLoader", "books")

# Where the Chroma vector store is persisted so we don't re-embed every run.
PERSIST_DIR = os.path.join(BASE_DIR, "rag_chroma_db")
COLLECTION_NAME = "pdf_rag_collection"

EMBEDDING_MODEL = "gemini-embedding-001"
CHAT_MODEL = "gemini-2.5-flash"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4


# --------------------------------------------------------------------------- #
# Environment / API key
# --------------------------------------------------------------------------- #
def configure_api_key() -> None:
    """Load the Gemini key from .env and expose it as GOOGLE_API_KEY.

    The project's .env file (DocumentLoader/.env) stores the key as
    GEMINI_API_KEY, but langchain_google_genai reads GOOGLE_API_KEY.
    """
    load_dotenv(os.path.join(BASE_DIR, "DocumentLoader", ".env"))
    load_dotenv(os.path.join(BASE_DIR, ".env"))  # optional override at root

    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        sys.exit(
            "ERROR: No API key found. Set GOOGLE_API_KEY (or GEMINI_API_KEY) "
            "in DocumentLoader/.env or your environment."
        )
    os.environ["GOOGLE_API_KEY"] = key.strip()


# --------------------------------------------------------------------------- #
# Step 1 + 2: Load PDFs and split into chunks
# --------------------------------------------------------------------------- #
def load_and_split() -> list:
    """Load all PDFs from PDF_FOLDER and split them into overlapping chunks."""
    if not os.path.isdir(PDF_FOLDER):
        sys.exit(f"ERROR: PDF folder not found: {PDF_FOLDER}")

    print(f"[1/4] Loading PDFs from: {PDF_FOLDER}")
    loader = DirectoryLoader(
        path=PDF_FOLDER,
        glob="**/*.pdf",
        loader_cls=PyMuPDF4LLMLoader,
        show_progress=True,
    )
    docs = loader.load()
    if not docs:
        sys.exit(f"ERROR: No PDFs found in {PDF_FOLDER}")
    print(f"      Loaded {len(docs)} page-documents.")

    print("[2/4] Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"      Produced {len(chunks)} chunks.")
    return chunks


# --------------------------------------------------------------------------- #
# Step 3: Build (or load) the vector store
# --------------------------------------------------------------------------- #
def get_vector_store(rebuild: bool = False) -> Chroma:
    """Return a Chroma vector store, building it from the PDFs if needed."""
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    already_indexed = os.path.isdir(PERSIST_DIR) and os.listdir(PERSIST_DIR)

    if already_indexed and not rebuild:
        print(f"[3/4] Loading existing vector store from: {PERSIST_DIR}")
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )

    chunks = load_and_split()
    print("[3/4] Embedding chunks and building Chroma vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
    )
    print(f"      Vector store persisted to: {PERSIST_DIR}")
    return vector_store


# --------------------------------------------------------------------------- #
# Step 4: Build the RAG chain (retriever + prompt + LLM)
# --------------------------------------------------------------------------- #
def format_docs(docs: list) -> str:
    """Join retrieved chunks into a single context string with source tags."""
    blocks = []
    for doc in docs:
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        page = doc.metadata.get("page", "?")
        blocks.append(f"[Source: {source}, page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(blocks)


def build_rag_chain(vector_store: Chroma):
    """Wire retriever -> prompt -> Gemini -> string output into one chain."""
    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K})

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that answers questions using ONLY "
                "the provided context from PDF documents. If the answer is not "
                "in the context, say you don't know. Cite the source file when "
                "you can.",
            ),
            (
                "human",
                "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0.2)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="PDF RAG app powered by Gemini.")
    parser.add_argument("question", nargs="*", help="Ask a single question and exit.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force re-loading and re-embedding of the PDFs.",
    )
    args = parser.parse_args()

    configure_api_key()
    vector_store = get_vector_store(rebuild=args.rebuild)
    chain = build_rag_chain(vector_store)
    print("[4/4] RAG chain ready.\n")

    # Single-shot mode: question passed on the command line.
    if args.question:
        question = " ".join(args.question)
        print(f"Q: {question}\n")
        print(f"A: {chain.invoke(question)}")
        return

    # Interactive mode.
    print("Ask a question about your PDFs (type 'exit' or 'quit' to stop).")
    while True:
        try:
            question = input("\nQ: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        print(f"\nA: {chain.invoke(question)}")


if __name__ == "__main__":
    main()
