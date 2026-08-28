import time
from typing import List, Dict, Any
import google.generativeai as genai


class ResponseGenerator:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", max_retries: int = 3):
        self.max_retries = max_retries
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        prompt = self._build_prompt(query, context_chunks)

        # Try a few times, because Gemini can briefly reject us with a
        # rate-limit error (429) when we send requests too quickly.
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                is_rate_limit = "429" in str(e) or "quota" in str(e).lower()
                # Give up if it's not a rate-limit error, or we're out of tries.
                if not is_rate_limit or attempt == self.max_retries - 1:
                    raise
                # Otherwise wait a bit (1s, then 2s, then 4s...) and try again.
                time.sleep(2 ** attempt)

    def _build_prompt(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        # Join all retrieved chunks into one context block the model can read.
        parts = []
        for c in chunks:
            parts.append(f"[Source: {c['source']}, Chunk {c['chunk_index']}]\n{c['text']}")

        if parts:
            context = "\n\n".join(parts)
        else:
            context = "No relevant context found."

        return f"""You are a helpful AI assistant. Answer using ONLY the context below.
Cite the source(s) you used. If the context is insufficient, say so clearly.

Context:
{context}

Question: {query}

Answer:"""
