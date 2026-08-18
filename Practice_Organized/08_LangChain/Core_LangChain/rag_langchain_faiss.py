"""
rag_langchain_faiss.py
========================
Same RAG pipeline as rag_pure_python.py, now built with LangChain's
abstractions (loaders, splitters, retriever, chain) + FAISS as the
vector store. FAISS runs entirely locally (no model download, no
server) so it's the easiest LangChain vectorstore to start with.

Model access goes through llm_provider.py -- same file as everywhere else
in this course. Runs unmodified on either laptop, whichever .env is active.

Requires: pip install langchain langchain-community langchain-text-splitters faiss-cpu --break-system-packages
"""

from llm_provider import get_chat_model, get_embeddings_model, MODEL_QWEN3_14B

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.chains import RetrievalQA


def build_qa_chain(raw_text: str) -> RetrievalQA:
    # 1. Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = [Document(page_content=c) for c in splitter.split_text(raw_text)]

    # 2. Embed + index (no HF hub calls -- get_embeddings_model() never touches HF)
    embeddings = get_embeddings_model()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 3. Save locally for reuse across runs (optional but useful for capstone)
    # vectorstore.save_local("faiss_index")
    # vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # 4. LLM
    llm = get_chat_model(model=MODEL_QWEN3_14B, max_tokens=500)

    # 5. Chain
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
