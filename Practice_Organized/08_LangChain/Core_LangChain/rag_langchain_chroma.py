"""
rag_langchain_chroma.py
==========================
Same pipeline again, this time with Chroma instead of FAISS.

IMPORTANT: Chroma's default embedding_function (if you don't pass one)
is sentence-transformers' all-MiniLM-L6-v2, which it tries to DOWNLOAD
from Hugging Face on first use. That is almost certainly what was
failing for you before. The fix: always pass embedding_function=
get_embeddings_model() explicitly, as done below — Chroma then never
touches its default and never calls out to HF.

Why bother with Chroma if FAISS already works? Chroma persists to disk
as a proper local database (metadata filtering, collections, delete/update
by id) which is closer to what you'll want for a real capstone app vs.
FAISS's simpler flat-file index. Good to know both.

Model access goes through llm_provider.py -- same file as everywhere else
in this course. Runs unmodified on either laptop, whichever .env is active.

Requires: pip install langchain langchain-chroma chromadb --break-system-packages
"""

from llm_provider import get_chat_model, get_embeddings_model, MODEL_QWEN3_14B

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.chains import RetrievalQA

PERSIST_DIR = "./chroma_db"


def build_qa_chain(raw_text: str, collection_name: str = "capstone_docs") -> RetrievalQA:
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = [Document(page_content=c) for c in splitter.split_text(raw_text)]

    embeddings = get_embeddings_model()  # <-- explicit, avoids Chroma's HF default

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=PERSIST_DIR,  # survives across script runs
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    llm = get_chat_model(model=MODEL_QWEN3_14B, max_tokens=500)
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


if __name__ == "__main__":
    raw_text = """
    Retrieval-Augmented Generation (RAG) combines a retriever and a generator.
    The retriever fetches relevant chunks from a vector store using embeddings.
    The generator, an LLM, uses those chunks as context to produce a grounded answer.
    Model Context Protocol (MCP) standardizes how LLMs call external tools and data
    sources through a client-server architecture, separating the model from the
    tool implementation. Agentic AI systems use an LLM as a controller that decides
    which tools to call, observes results, and plans next steps in a loop.
    """

    qa_chain = build_qa_chain(raw_text)
    question = "How does RAG differ from an agentic AI loop?"
    result = qa_chain.invoke({"query": question})
    print("Q:", question)
    print("A:", result["result"])
