"""
rag_pure_python.py
===================
RAG with ZERO retrieval-framework abstractions: no LangChain retriever/chain/
vectorstore classes, no Chroma/FAISS library. This is the version to study
first -- every moving part is visible: chunking, embedding, similarity
search, prompt construction, generation.

Once this makes sense, rag_langchain_faiss.py and rag_langchain_chroma.py
will feel like "the same steps, now with less boilerplate."

Model access goes through llm_provider.py -- the same file used everywhere
else in this course, so this script runs unmodified on your personal laptop
(real OpenAI) or your office laptop (in-house Qwen3/Jina), whichever .env
is active. See llm_provider.py's own docstring for what it fixes and why.
"""

import numpy as np
from langchain_core.messages import SystemMessage, HumanMessage
from llm_provider import get_chat_model, get_embeddings_model, MODEL_QWEN3_14B


# 1. Chunking ---------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 200, overlap: int = 20) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]


# 2. In-memory vector store ---------------------------------------------------
class SimpleVectorStore:
    def __init__(self):
        # get_embeddings_model() already resolves to the right backend
        # (in-house Jina on office, OpenAI embeddings on personal) -- no
        # model= kwarg needed here, unlike the old direct get_embedding() call.
        self.embedder = get_embeddings_model()
        self.texts: list[str] = []
        self.vectors: list[np.ndarray] = []

    def add(self, texts: list[str]) -> None:
        vecs = self.embedder.embed_documents(texts)
        for t, vec in zip(texts, vecs):
            self.texts.append(t)
            self.vectors.append(np.array(vec))

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        q_vec = np.array(self.embedder.embed_query(query))
        scores = []
        for text, vec in zip(self.texts, self.vectors):
            # cosine similarity
            sim = np.dot(q_vec, vec) / (np.linalg.norm(q_vec) * np.linalg.norm(vec) + 1e-8)
            scores.append((text, float(sim)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]


# 3. Generation ---------------------------------------------------------------
def generate_answer(question: str, context_chunks: list[str], model: str = MODEL_QWEN3_14B) -> str:
    context = "\n\n".join(context_chunks)
    system_prompt = "Answer using only the provided context. If the context doesn't contain the answer, say so."
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    llm = get_chat_model(model=model, max_tokens=500)
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    return response.content


# 4. Demo ---------------------------------------------------------------------
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

    store = SimpleVectorStore()
    store.add(chunk_text(raw_text))

    question = "How does RAG differ from an agentic AI loop?"
    top_chunks = [text for text, score in store.search(question, k=2)]
    answer = generate_answer(question, top_chunks)

    print("Q:", question)
    print("Retrieved chunks:", top_chunks)
    print("A:", answer)



# 4. Demo ---------------------------------------------------------------------
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

    store = SimpleVectorStore()
    store.add(chunk_text(raw_text))

    question = "How does RAG differ from an agentic AI loop?"
    top_chunks = [text for text, score in store.search(question, k=2)]
    answer = generate_answer(question, top_chunks)

    print("Q:", question)
    print("Retrieved chunks:", top_chunks)
    print("A:", answer)
