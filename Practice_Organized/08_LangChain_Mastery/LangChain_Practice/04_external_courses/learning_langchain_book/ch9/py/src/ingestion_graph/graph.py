import json
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

from ingestion_graph.configuration import IndexConfiguration
from ingestion_graph.state import IndexState, reduce_docs

from shared.retrieval import make_retriever


async def ingest_docs(state: IndexState, config: Optional[RunnableConfig] = None) -> dict[str, str]:
    if not config:
        raise ValueError("Configuration required to run index_docs.")

    configuration = IndexConfiguration.from_runnable_config(config)
    docs = state["docs"]
    if not docs:
        with open(configuration.docs_file, encoding="utf-8") as file_content:
            serialized_docs = json.loads(file_content.read())
            docs = reduce_docs([], serialized_docs)
    else:
        docs = reduce_docs([], docs)

    with make_retriever(configuration) as retriever:
        await retriever.aadd_documents(docs)

    return {"docs": "delete"}

# Define the graph
builder = StateGraph(IndexState, config_schema=IndexConfiguration)
builder.add_node(ingest_docs)
builder.add_edge(START, "ingest_docs")
builder.add_edge("ingest_docs", END)

# Compile into a graph object that you can invoke and deploy.
graph = builder.compile()
graph.name = "IngestionGraph"
