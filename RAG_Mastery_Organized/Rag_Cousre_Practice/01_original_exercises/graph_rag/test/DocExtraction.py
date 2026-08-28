import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
import time
import random

# Load environment variables from .env file
load_dotenv()

# Import required libraries
from docling.document_converter import DocumentConverter
from neo4j import GraphDatabase
import google.generativeai as genai
import numpy as np

class RAGSystem:
    """
    A complete RAG (Retrieval-Augmented Generation) system that:
    1. Extracts content from PDFs using Docling
    2. Stores embeddings in Neo4j graph database
    3. Retrieves relevant context and generates responses using Gemini
    """
    
    def __init__(self):
        """Initialize the RAG system with API keys and database connections."""
        # Fetch API keys and connection details from environment variables
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")  # Database name
        self.neo4j_instance = os.getenv("NEO4J_INSTANCE", "neo4j")  # Instance name
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Validate required environment variables
        if not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD not found in environment variables")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize Neo4j driver with instance and database
        self.driver = GraphDatabase.driver(
            self.neo4j_uri,
            auth=(self.neo4j_user, self.neo4j_password)
        )
        
        print(f"Connected to Neo4j instance: {self.neo4j_instance}")
        print(f"Using database: {self.neo4j_database}")
        
        # Configure Gemini API
        genai.configure(api_key=self.gemini_api_key)
        
        # Use the latest free embedding model (high rate limits: 1500 RPM)
        self.embedding_model = "models/text-embedding-004"
        
        # Choose generation model based on your needs:
        # Option 1: gemini-1.5-flash - Faster, 15 RPM, 1500 requests/day (RECOMMENDED for RAG)
        # Option 2: gemini-1.5-pro - More intelligent, 2 RPM, 50 requests/day
        self.generation_model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"Using embedding model: {self.embedding_model}")
        print(f"Using generation model: gemini-1.5-flash")
        
        # Initialize Docling document converter
        self.doc_converter = DocumentConverter()
        
        # Setup Neo4j vector index
        self._setup_neo4j_schema()
    
    def _setup_neo4j_schema(self):
        """Create Neo4j schema with vector index for similarity search."""
        with self.driver.session(database=self.neo4j_database) as session:
            # Create constraint for unique document chunks
            session.run("""
                CREATE CONSTRAINT chunk_id IF NOT EXISTS
                FOR (c:Chunk) REQUIRE c.id IS UNIQUE
            """)
            
            # Create vector index for similarity search
            # Note: Vector indexes require Neo4j 5.11+ with vector search support
            try:
                session.run("""
                    CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS
                    FOR (c:Chunk) ON (c.embedding)
                    OPTIONS {indexConfig: {
                        `vector.dimensions`: 768,
                        `vector.similarity_function`: 'cosine'
                    }}
                """)
            except Exception as e:
                print(f"Vector index creation note: {e}")
                print("If using Neo4j version < 5.11, you'll need to upgrade for vector search")
    
    def extract_pdf_content(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract content from PDF using Docling.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        print(f"Extracting content from: {pdf_path}")
        
        # Convert PDF document
        result = self.doc_converter.convert(pdf_path)
        
        chunks = []
        chunk_id = 0
        
        # Extract text from document structure
        for element in result.document.iterate_items():
            text = element.text.strip() if hasattr(element, 'text') else ""
            
            if text and len(text) > 50:  # Only store meaningful chunks
                chunks.append({
                    "id": f"{Path(pdf_path).stem}_chunk_{chunk_id}",
                    "text": text,
                    "source": pdf_path,
                    "chunk_index": chunk_id,
                    "metadata": {
                        "element_type": element.__class__.__name__,
                        "length": len(text)
                    }
                })
                chunk_id += 1
        
        print(f"Extracted {len(chunks)} chunks from PDF")
        return chunks
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using Gemini API.
        Includes retry logic for rate limiting on free tier.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use Gemini's embedding model (Free tier: 1500 requests/minute)
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    # Rate limit hit - exponential backoff
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Rate limit hit. Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise Exception("Rate limit exceeded. Please wait and try again.")
                else:
                    raise e
    
    def store_chunks_in_neo4j(self, chunks: List[Dict[str, Any]]):
        """
        Store text chunks with embeddings in Neo4j graph database.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
        """
        print("Storing chunks in Neo4j with embeddings...")
        
        with self.driver.session(database=self.neo4j_database) as session:
            for chunk in chunks:
                # Generate embedding for the chunk
                embedding = self.generate_embedding(chunk["text"])
                
                # Store chunk with embedding in Neo4j
                session.run("""
                    MERGE (c:Chunk {id: $id})
                    SET c.text = $text,
                        c.source = $source,
                        c.chunk_index = $chunk_index,
                        c.embedding = $embedding,
                        c.metadata = $metadata
                """, {
                    "id": chunk["id"],
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "chunk_index": chunk["chunk_index"],
                    "embedding": embedding,
                    "metadata": str(chunk["metadata"])
                })
                
                print(f"Stored chunk: {chunk['id']}")
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve most relevant chunks for a query using vector similarity.
        
        Args:
            query: User query text
            top_k: Number of top results to return
            
        Returns:
            List of relevant chunks with similarity scores
        """
        # Generate embedding for the query
        query_embedding = self.generate_embedding(query)
        
        with self.driver.session(database=self.neo4j_database) as session:
            # Perform vector similarity search
            # For Neo4j < 5.11, use alternative approach with manual similarity calculation
            result = session.run("""
                MATCH (c:Chunk)
                WITH c, 
                     reduce(dot = 0.0, i IN range(0, size(c.embedding)-1) | 
                        dot + c.embedding[i] * $query_embedding[i]) AS similarity
                RETURN c.id AS id, 
                       c.text AS text, 
                       c.source AS source,
                       c.chunk_index AS chunk_index,
                       similarity
                ORDER BY similarity DESC
                LIMIT $top_k
            """, {
                "query_embedding": query_embedding,
                "top_k": top_k
            })
            
            chunks = []
            for record in result:
                chunks.append({
                    "id": record["id"],
                    "text": record["text"],
                    "source": record["source"],
                    "chunk_index": record["chunk_index"],
                    "similarity": record["similarity"]
                })
            
            return chunks
    
    def generate_response(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate response using Gemini based on query and retrieved context.
        Includes retry logic for free tier rate limits.
        
        Args:
            query: User query
            context_chunks: Retrieved relevant chunks
            
        Returns:
            Generated response text
        """
        # Build context from retrieved chunks
        context = "\n\n".join([
            f"[Source: {chunk['source']}, Chunk {chunk['chunk_index']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Create prompt with context and query
        prompt = f"""Based on the following context, please answer the question.

Context:
{context}

Question: {query}

Answer: Provide a comprehensive answer based only on the information in the context above. If the context doesn't contain enough information to answer the question, say so."""
        
        # Generate response with retry logic for free tier
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Free tier limits: gemini-1.5-flash = 15 RPM, 1500 requests/day
                response = self.generation_model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Rate limit hit. Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise Exception("Rate limit exceeded. Please wait and try again.")
                else:
                    raise e
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve relevant chunks and generate response.
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary with response and source chunks
        """
        print(f"\nProcessing query: {question}")
        
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(question, top_k)
        print(f"Retrieved {len(relevant_chunks)} relevant chunks")
        
        # Generate response
        response = self.generate_response(question, relevant_chunks)
        
        return {
            "question": question,
            "answer": response,
            "sources": relevant_chunks
        }
    
    def close(self):
        """Close Neo4j database connection."""
        self.driver.close()
        print("Neo4j connection closed")


# Example usage
if __name__ == "__main__":
    # Initialize RAG system
    rag = RAGSystem()
    
    # Example 1: Extract and store PDF content
    pdf_file = "your_document.pdf"  # Replace with your PDF path
    
    if os.path.exists(pdf_file):
        # Extract content from PDF
        chunks = rag.extract_pdf_content(pdf_file)
        
        # Store chunks in Neo4j with embeddings
        rag.store_chunks_in_neo4j(chunks)
    
    # Example 2: Query the RAG system
    question = "What are the main topics discussed in the document?"
    result = rag.query(question, top_k=3)
    
    print("\n" + "="*80)
    print("QUESTION:", result["question"])
    print("="*80)
    print("\nANSWER:")
    print(result["answer"])
    print("\n" + "="*80)
    print("SOURCES:")
    for i, source in enumerate(result["sources"], 1):
        print(f"\n{i}. {source['source']} (Chunk {source['chunk_index']})")
        print(f"   Similarity: {source['similarity']:.4f}")
        print(f"   Text preview: {source['text'][:200]}...")
    
    # Close connection
    rag.close()