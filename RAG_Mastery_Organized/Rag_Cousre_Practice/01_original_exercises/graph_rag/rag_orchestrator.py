from typing import List, Dict, Any, Optional
from config import Config
from pdf_processor import PDFProcessor
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from response_generator import ResponseGenerator


class RAGOrchestrator:
    def __init__(self, config: Config = None):
        self.config = config or Config()

        self.pdf_processor = PDFProcessor(min_chunk_length=self.config.chunk_min_length)
        self.embedder = EmbeddingGenerator(model=self.config.embedding_model)
        self.vector_store = VectorStore(
            uri=self.config.neo4j_uri,
            user=self.config.neo4j_user,
            password=self.config.neo4j_password,
            database=self.config.neo4j_database,
        )
        self.responder = ResponseGenerator(
            api_key=self.config.gemini_api_key,
            model=self.config.generation_model,
            max_retries=self.config.max_retries,
        )

    def process_and_store_pdf(self, pdf_path: str) -> Dict[str, Any]:
        
        chunks = self.pdf_processor.extract_chunks(pdf_path)
        if not chunks:
            return {"success": False, "message": "No chunks extracted", "chunks_processed": 0}

        embeddings = []
        for c in chunks:
            embeddings.append(self.embedder.generate_document_embedding(c["text"]))
        self.vector_store.store_chunks_batch(chunks, embeddings)

        stats = self.pdf_processor.get_chunk_statistics(chunks)
        return {
            "success": True,
            "message": f"Processed {len(chunks)} chunks",
            "chunks_processed": len(chunks),
            "statistics": stats,
        }

    def query(self, question: str, top_k: int = None) -> Dict[str, Any]:
        top_k = top_k or self.config.top_k_results

        query_embedding = self.embedder.generate_query_embedding(question)
        relevant_chunks = self.vector_store.search_similar(query_embedding, top_k)

        if not relevant_chunks:
            return {
                "question": question,
                "answer": "No relevant information found in the knowledge base.",
                "sources": [],
            }

        answer = self.responder.generate(question, relevant_chunks)
        return {"question": question, "answer": answer, "sources": relevant_chunks}

    def get_database_info(self) -> Dict[str, Any]:
        sources = self.vector_store.get_all_sources()
        return {
            "total_chunks": self.vector_store.get_chunk_count(),
            "total_documents": len(sources),
            "documents": sources,
        }

    def delete_document(self, source: str):
        self.vector_store.delete_by_source(source)

    def close(self):
        self.vector_store.close()
