"""
Setup script to create all RAG system files automatically.
Run this script to generate all necessary Python modules.
"""

import os

# Dictionary containing all file contents
FILES = {
    "config.py": '''"""
Configuration module for RAG system.
Handles loading and validating environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for RAG system."""
    
    def __init__(self):
        """Initialize and validate configuration."""
        # Neo4j Configuration
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.neo4j_instance = os.getenv("NEO4J_INSTANCE", "neo4j")
        
        # Gemini API Configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Model Configuration
        self.embedding_model = "models/text-embedding-004"
        self.generation_model = "gemini-1.5-flash"
        
        # RAG Configuration
        self.chunk_min_length = 50  # Minimum chunk length in characters
        self.top_k_results = 5  # Default number of results to retrieve
        self.max_retries = 3  # Max retries for API calls
        
        # Validate required settings
        self._validate()
    
    def _validate(self):
        """Validate that required configuration values are set."""
        if not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD not found in environment variables")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    def display_config(self):
        """Display current configuration (without sensitive data)."""
        print("="*60)
        print("RAG System Configuration")
        print("="*60)
        print(f"Neo4j URI: {self.neo4j_uri}")
        print(f"Neo4j User: {self.neo4j_user}")
        print(f"Neo4j Database: {self.neo4j_database}")
        print(f"Neo4j Instance: {self.neo4j_instance}")
        print(f"Embedding Model: {self.embedding_model}")
        print(f"Generation Model: {self.generation_model}")
        print(f"Chunk Min Length: {self.chunk_min_length}")
        print(f"Top K Results: {self.top_k_results}")
        print("="*60)
''',

    "pdf_processor.py": '''"""
PDF processing module using Docling.
Handles PDF extraction and chunking.
"""

from pathlib import Path
from typing import List, Dict, Any
from docling.document_converter import DocumentConverter

class PDFProcessor:
    """Class for processing PDF documents and extracting chunks."""
    
    def __init__(self, min_chunk_length: int = 50):
        """
        Initialize PDF processor.
        
        Args:
            min_chunk_length: Minimum length of text chunks to extract
        """
        self.min_chunk_length = min_chunk_length
        self.doc_converter = DocumentConverter()
    
    def extract_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text chunks from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        print(f"📄 Extracting content from: {pdf_path}")
        
        try:
            # Convert PDF document using Docling
            result = self.doc_converter.convert(pdf_path)
            
            chunks = []
            chunk_id = 0
            
            # Extract text from document structure
            for element in result.document.iterate_items():
                text = element.text.strip() if hasattr(element, 'text') else ""
                
                # Only store meaningful chunks (longer than minimum length)
                if text and len(text) > self.min_chunk_length:
                    chunks.append({
                        "id": f"{Path(pdf_path).stem}_chunk_{chunk_id}",
                        "text": text,
                        "source": Path(pdf_path).name,  # Store just filename
                        "chunk_index": chunk_id,
                        "metadata": {
                            "element_type": element.__class__.__name__,
                            "length": len(text)
                        }
                    })
                    chunk_id += 1
            
            print(f"✅ Extracted {len(chunks)} chunks from PDF")
            return chunks
            
        except Exception as e:
            print(f"❌ Error extracting PDF: {str(e)}")
            raise
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about extracted chunks.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {"total_chunks": 0, "total_chars": 0, "avg_chunk_size": 0}
        
        total_chars = sum(chunk["metadata"]["length"] for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks)
        
        return {
            "total_chunks": len(chunks),
            "total_chars": total_chars,
            "avg_chunk_size": round(avg_chunk_size, 2),
            "min_chunk_size": min(chunk["metadata"]["length"] for chunk in chunks),
            "max_chunk_size": max(chunk["metadata"]["length"] for chunk in chunks)
        }
''',

    "embeddings.py": '''"""
Embedding generation module using Google Gemini.
Handles text-to-vector conversion with retry logic.
"""

import time
import random
from typing import List
import google.generativeai as genai

class EmbeddingGenerator:
    """Class for generating embeddings using Gemini API."""
    
    def __init__(self, api_key: str, model: str = "models/text-embedding-004", max_retries: int = 3):
        """
        Initialize embedding generator.
        
        Args:
            api_key: Gemini API key
            model: Embedding model to use
            max_retries: Maximum number of retries for rate limiting
        """
        self.api_key = api_key
        self.model = model
        self.max_retries = max_retries
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        print(f"🤖 Initialized Gemini Embedding Model: {self.model}")
    
    def generate(self, text: str, task_type: str = "retrieval_document") -> List[float]:
        """
        Generate embedding vector for text with retry logic.
        
        Args:
            text: Input text to embed
            task_type: Type of task (retrieval_document or retrieval_query)
            
        Returns:
            Embedding vector as list of floats
        """
        for attempt in range(self.max_retries):
            try:
                # Generate embedding using Gemini API
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type=task_type
                )
                return result['embedding']
                
            except Exception as e:
                # Handle rate limiting with exponential backoff
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"⏳ Rate limit hit. Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise Exception("❌ Rate limit exceeded. Please wait and try again.")
                else:
                    print(f"❌ Error generating embedding: {str(e)}")
                    raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        return self.generate(query, task_type="retrieval_query")
    
    def generate_document_embedding(self, document: str) -> List[float]:
        """
        Generate embedding for a document.
        
        Args:
            document: Document text
            
        Returns:
            Embedding vector
        """
        return self.generate(document, task_type="retrieval_document")
''',

    "vector_store.py": '''"""
Neo4j vector database module.
Handles storing and retrieving embeddings from Neo4j.
"""

from typing import List, Dict, Any
from neo4j import GraphDatabase

class VectorStore:
    """Class for managing vector storage in Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        """
        Initialize Neo4j vector store.
        
        Args:
            uri: Neo4j connection URI
            user: Neo4j username
            password: Neo4j password
            database: Database name
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        
        # Initialize Neo4j driver
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )
        
        print(f"🗄️  Connected to Neo4j database: {self.database}")
        
        # Setup database schema
        self._setup_schema()
    
    def _setup_schema(self):
        """Create Neo4j schema with constraints and vector index."""
        with self.driver.session(database=self.database) as session:
            # Create unique constraint for chunk IDs
            session.run("""
                CREATE CONSTRAINT chunk_id IF NOT EXISTS
                FOR (c:Chunk) REQUIRE c.id IS UNIQUE
            """)
            
            # Create vector index for similarity search
            # Note: Requires Neo4j 5.11+ with vector search support
            try:
                session.run("""
                    CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS
                    FOR (c:Chunk) ON (c.embedding)
                    OPTIONS {indexConfig: {
                        `vector.dimensions`: 768,
                        `vector.similarity_function`: 'cosine'
                    }}
                """)
                print("✅ Vector index created/verified")
            except Exception as e:
                print(f"⚠️  Vector index note: {e}")
                print("   Manual similarity calculation will be used")
    
    def store_chunk(self, chunk_id: str, text: str, embedding: List[float], 
                   source: str, chunk_index: int, metadata: Dict[str, Any]):
        """
        Store a single chunk with embedding in Neo4j.
        
        Args:
            chunk_id: Unique chunk identifier
            text: Chunk text content
            embedding: Embedding vector
            source: Source document name
            chunk_index: Index of chunk in document
            metadata: Additional metadata
        """
        with self.driver.session(database=self.database) as session:
            session.run("""
                MERGE (c:Chunk {id: $id})
                SET c.text = $text,
                    c.source = $source,
                    c.chunk_index = $chunk_index,
                    c.embedding = $embedding,
                    c.metadata = $metadata
            """, {
                "id": chunk_id,
                "text": text,
                "source": source,
                "chunk_index": chunk_index,
                "embedding": embedding,
                "metadata": str(metadata)
            })
    
    def store_chunks_batch(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Store multiple chunks with embeddings in batch.
        
        Args:
            chunks: List of chunk dictionaries
            embeddings: List of embedding vectors
        """
        print(f"💾 Storing {len(chunks)} chunks in Neo4j...")
        
        for chunk, embedding in zip(chunks, embeddings):
            self.store_chunk(
                chunk_id=chunk["id"],
                text=chunk["text"],
                embedding=embedding,
                source=chunk["source"],
                chunk_index=chunk["chunk_index"],
                metadata=chunk["metadata"]
            )
            print(f"   ✓ Stored: {chunk['id']}")
        
        print(f"✅ All {len(chunks)} chunks stored successfully!")
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of similar chunks with similarity scores
        """
        with self.driver.session(database=self.database) as session:
            # Perform cosine similarity search using dot product
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
                    "similarity": float(record["similarity"])
                })
            
            return chunks
    
    def get_all_sources(self) -> List[str]:
        """
        Get list of all document sources in the database.
        
        Returns:
            List of unique source names
        """
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (c:Chunk)
                RETURN DISTINCT c.source AS source
                ORDER BY source
            """)
            return [record["source"] for record in result]
    
    def get_chunk_count(self) -> int:
        """
        Get total number of chunks in database.
        
        Returns:
            Total chunk count
        """
        with self.driver.session(database=self.database) as session:
            result = session.run("MATCH (c:Chunk) RETURN count(c) AS count")
            return result.single()["count"]
    
    def delete_by_source(self, source: str):
        """
        Delete all chunks from a specific source.
        
        Args:
            source: Source document name
        """
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (c:Chunk {source: $source})
                DELETE c
                RETURN count(c) AS deleted_count
            """, {"source": source})
            deleted = result.single()["deleted_count"]
            print(f"🗑️  Deleted {deleted} chunks from source: {source}")
    
    def close(self):
        """Close Neo4j database connection."""
        self.driver.close()
        print("🔌 Neo4j connection closed")
''',

    "response_generator.py": '''"""
Response generation module using Google Gemini.
Handles generating responses from retrieved context.
"""

import time
import random
from typing import List, Dict, Any
import google.generativeai as genai

class ResponseGenerator:
    """Class for generating responses using Gemini LLM."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", max_retries: int = 3):
        """
        Initialize response generator.
        
        Args:
            api_key: Gemini API key
            model: Generation model to use
            max_retries: Maximum number of retries for rate limiting
        """
        self.api_key = api_key
        self.model_name = model
        self.max_retries = max_retries
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"🤖 Initialized Gemini Generation Model: {self.model_name}")
    
    def generate(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate response based on query and retrieved context.
        
        Args:
            query: User query
            context_chunks: Retrieved relevant chunks
            
        Returns:
            Generated response text
        """
        # Build context from retrieved chunks
        context = self._build_context(context_chunks)
        
        # Create prompt with context and query
        prompt = self._create_prompt(query, context)
        
        # Generate response with retry logic
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                # Handle rate limiting with exponential backoff
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"⏳ Rate limit hit. Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                    else:
                        raise Exception("❌ Rate limit exceeded. Please wait and try again.")
                else:
                    print(f"❌ Error generating response: {str(e)}")
                    raise
    
    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Build formatted context from chunks.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Context {i} - Source: {chunk['source']}, Chunk {chunk['chunk_index']}]\\n"
                f"{chunk['text']}\\n"
            )
        
        return "\\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create prompt for the LLM.
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful AI assistant answering questions based on provided context.

Context Information:
{context}

User Question: {query}

Instructions:
- Answer the question using ONLY the information provided in the context above
- Be accurate and specific
- If the context doesn't contain enough information to fully answer the question, acknowledge this
- Cite which context sources you used in your answer
- Keep your answer clear and concise

Answer:"""
        
        return prompt
''',

    "rag_orchestrator.py": '''"""
RAG Orchestrator - Main module that coordinates all RAG components.
"""

from typing import List, Dict, Any
from config import Config
from pdf_processor import PDFProcessor
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from response_generator import ResponseGenerator

class RAGOrchestrator:
    """Main orchestrator class that coordinates all RAG components."""
    
    def __init__(self, config: Config = None):
        """
        Initialize RAG orchestrator with all components.
        
        Args:
            config: Configuration object (creates default if None)
        """
        # Load configuration
        self.config = config if config else Config()
        
        print("\\n" + "="*60)
        print("🚀 Initializing RAG System Components")
        print("="*60)
        
        # Initialize all components
        self.pdf_processor = PDFProcessor(
            min_chunk_length=self.config.chunk_min_length
        )
        
        self.embedding_generator = EmbeddingGenerator(
            api_key=self.config.gemini_api_key,
            model=self.config.embedding_model,
            max_retries=self.config.max_retries
        )
        
        self.vector_store = VectorStore(
            uri=self.config.neo4j_uri,
            user=self.config.neo4j_user,
            password=self.config.neo4j_password,
            database=self.config.neo4j_database
        )
        
        self.response_generator = ResponseGenerator(
            api_key=self.config.gemini_api_key,
            model=self.config.generation_model,
            max_retries=self.config.max_retries
        )
        
        print("="*60)
        print("✅ RAG System Initialized Successfully!")
        print("="*60 + "\\n")
    
    def process_and_store_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: Extract PDF, generate embeddings, store in Neo4j.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with processing statistics
        """
        print(f"\\n📚 Processing PDF: {pdf_path}")
        print("-" * 60)
        
        # Step 1: Extract chunks from PDF
        chunks = self.pdf_processor.extract_chunks(pdf_path)
        
        if not chunks:
            return {
                "success": False,
                "message": "No chunks extracted from PDF",
                "chunks_processed": 0
            }
        
        # Get statistics
        stats = self.pdf_processor.get_chunk_statistics(chunks)
        print(f"📊 Statistics: {stats}")
        
        # Step 2: Generate embeddings for all chunks
        print(f"\\n🔄 Generating embeddings for {len(chunks)} chunks...")
        embeddings = []
        for i, chunk in enumerate(chunks, 1):
            embedding = self.embedding_generator.generate_document_embedding(chunk["text"])
            embeddings.append(embedding)
            if i % 10 == 0:
                print(f"   Progress: {i}/{len(chunks)} embeddings generated")
        
        # Step 3: Store chunks with embeddings in Neo4j
        print(f"\\n💾 Storing chunks in Neo4j...")
        self.vector_store.store_chunks_batch(chunks, embeddings)
        
        print("-" * 60)
        print(f"✅ PDF Processing Complete!")
        
        return {
            "success": True,
            "message": f"Successfully processed {len(chunks)} chunks",
            "chunks_processed": len(chunks),
            "statistics": stats
        }
    
    def query(self, question: str, top_k: int = None) -> Dict[str, Any]:
        """
        Query the RAG system: retrieve relevant chunks and generate response.
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve (uses config default if None)
            
        Returns:
            Dictionary with question, answer, and source chunks
        """
        if top_k is None:
            top_k = self.config.top_k_results
        
        print(f"\\n🔍 Processing Query: {question}")
        print("-" * 60)
        
        # Step 1: Generate query embedding
        print("🔄 Generating query embedding...")
        query_embedding = self.embedding_generator.generate_query_embedding(question)
        
        # Step 2: Retrieve relevant chunks from Neo4j
        print(f"🔍 Searching for top {top_k} relevant chunks...")
        relevant_chunks = self.vector_store.search_similar(query_embedding, top_k)
        
        if not relevant_chunks:
            print("⚠️  No relevant chunks found")
            return {
                "question": question,
                "answer": "I couldn't find any relevant information in the knowledge base to answer your question.",
                "sources": []
            }
        
        print(f"✅ Found {len(relevant_chunks)} relevant chunks")
        
        # Step 3: Generate response using LLM
        print("🤖 Generating response...")
        answer = self.response_generator.generate(question, relevant_chunks)
        
        print("-" * 60)
        print("✅ Query Processing Complete!")
        
        return {
            "question": question,
            "answer": answer,
            "sources": relevant_chunks
        }
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the current database state.
        
        Returns:
            Dictionary with database statistics
        """
        chunk_count = self.vector_store.get_chunk_count()
        sources = self.vector_store.get_all_sources()
        
        return {
            "total_chunks": chunk_count,
            "total_documents": len(sources),
            "documents": sources
        }
    
    def delete_document(self, source: str):
        """
        Delete all chunks from a specific document.
        
        Args:
            source: Source document name
        """
        self.vector_store.delete_by_source(source)
    
    def close(self):
        """Close all connections."""
        self.vector_store.close()
        print("👋 RAG System shut down successfully")
''',
}

def create_files():
    """Create all project files."""
    print("="*60)
    print("🚀 RAG System Project Setup")
    print("="*60)
    print("\nCreating project files...\n")
    
    created_files = []
    
    for filename, content in FILES.items():
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {filename}")
            created_files.append(filename)
        except Exception as e:
            print(f"❌ Error creating {filename}: {str(e)}")
    
    print("\n" + "="*60)
    print(f"✅ Successfully created {len(created_files)} files!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Create .env file with your credentials")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python app.py")
    print("\n" + "="*60)

if __name__ == "__main__":
    create_files()