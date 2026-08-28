from typing import List, Dict, Any
from neo4j import GraphDatabase


class VectorStore:
    def __init__(self, uri: str, user: str, password: str, database: str = "graphragdb"):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._setup_schema()

    def _setup_schema(self):
        with self.driver.session(database=self.database) as session:
            session.run("""
                CREATE CONSTRAINT chunk_id IF NOT EXISTS
                FOR (c:Chunk) REQUIRE c.id IS UNIQUE
            """)
            try:
                session.run("""
                    CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS
                    FOR (c:Chunk) ON (c.embedding)
                    OPTIONS {indexConfig: {
                        `vector.dimensions`: 768,
                        `vector.similarity_function`: 'cosine'
                    }}
                """)
            except Exception:
                pass  # older Neo4j — manual cosine fallback used in search

    def store_chunks_batch(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Store all chunks in a single transaction using UNWIND."""
        params = []
        for c, emb in zip(chunks, embeddings):
            params.append({
                "id": c["id"],
                "text": c["text"],
                "source": c["source"],
                "chunk_index": c["chunk_index"],
                "embedding": emb,
                "metadata": str(c["metadata"]),
            })
        with self.driver.session(database=self.database) as session:
            session.run("""
                UNWIND $params AS p
                MERGE (c:Chunk {id: p.id})
                SET c.text       = p.text,
                    c.source     = p.source,
                    c.chunk_index = p.chunk_index,
                    c.embedding  = p.embedding,
                    c.metadata   = p.metadata
            """, {"params": params})

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (c:Chunk)
                WITH c,
                     reduce(dot = 0.0, i IN range(0, size(c.embedding)-1) |
                        dot + c.embedding[i] * $qe[i]) AS similarity
                RETURN c.id AS id, c.text AS text, c.source AS source,
                       c.chunk_index AS chunk_index, similarity
                ORDER BY similarity DESC
                LIMIT $top_k
            """, {"qe": query_embedding, "top_k": top_k})

            chunks = []
            for r in result:
                chunks.append({
                    "id": r["id"],
                    "text": r["text"],
                    "source": r["source"],
                    "chunk_index": r["chunk_index"],
                    "similarity": float(r["similarity"]),
                })
            return chunks

    def get_all_sources(self) -> List[str]:
        with self.driver.session(database=self.database) as session:
            result = session.run(
                "MATCH (c:Chunk) RETURN DISTINCT c.source AS source ORDER BY source"
            )
            return [r["source"] for r in result]

    def get_chunk_count(self) -> int:
        with self.driver.session(database=self.database) as session:
            return session.run("MATCH (c:Chunk) RETURN count(c) AS count").single()["count"]

    def delete_by_source(self, source: str):
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (c:Chunk {source: $source}) DELETE c", {"source": source})

    def close(self):
        self.driver.close()
