from typing import Annotated
from langgraph.graph import MessagesState
from langchain_core.documents import Document

from shared.state import reduce_docs


class AgentState(MessagesState):
    query: str
    route: str
    documents: Annotated[list[Document], reduce_docs]

