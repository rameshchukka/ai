import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "graphragdb")

        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Local HuggingFace embedding model (no API calls). 768-dim output.
        self.embedding_model = "all-mpnet-base-v2"
        self.generation_model = "gemini-2.5-flash"

        self.chunk_min_length = 20
        self.top_k_results = 5
        self.max_retries = 3

        if not self.neo4j_password:
            raise ValueError("NEO4J_PASSWORD not set in environment")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

    def display(self):
        print(f"Neo4j: {self.neo4j_uri} / db={self.neo4j_database}")
        print(f"Embedding: {self.embedding_model}")
        print(f"Generation: {self.generation_model}")
