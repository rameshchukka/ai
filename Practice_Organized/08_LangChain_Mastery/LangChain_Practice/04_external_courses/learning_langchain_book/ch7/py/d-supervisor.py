from typing import Literal

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from pydantic import BaseModel


class SupervisorDecision(BaseModel):
    next: Literal["researcher", "coder", "FINISH"]


# Initialize model
model = ChatOpenAI(model="gpt-4", temperature=0)
model = model.with_structured_output(SupervisorDecision)

# Define available agents
agents = ["researcher", "coder"]

# Define system prompts
system_prompt_part_1 = f"""You are a supervisor tasked with managing a conversation between the  
following workers: {agents}. Given the following user request,  
respond with the worker to act next. Each worker will perform a  
task and respond with their results and status. When finished,  
respond with FINISH."""

system_prompt_part_2 = f"""Given the conversation above, who should act next? Or should we FINISH? Select one of: {", ".join(agents)}, FINISH"""


def supervisor(state):
    messages = [
        ("system", system_prompt_part_1),
        *state["messages"],
        ("system", system_prompt_part_2),
    ]
    return model.invoke(messages)


# Define agent state
class AgentState(MessagesState):
    next: Literal["researcher", "coder", "FINISH"]


# Define agent functions
def researcher(state: AgentState):
    # In a real implementation, this would do research tasks
    response = model.invoke(
        [
            {
                "role": "system",
                "content": "You are a research assistant. Analyze the request and provide relevant information.",
            },
            {"role": "user", "content": state["messages"][0].content},
        ]
    )
    return {"messages": [response]}


def coder(state: AgentState):
    # In a real implementation, this would write code
    response = model.invoke(
        [
            {
                "role": "system",
                "content": "You are a coding assistant. Implement the requested functionality.",
            },
            {"role": "user", "content": state["messages"][0].content},
        ]
    )
    return {"messages": [response]}


# Build the graph
builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("coder", coder)

builder.add_edge(START, "supervisor")
# Route to one of the agents or exit based on the supervisor's decision
builder.add_conditional_edges("supervisor", lambda state: state["next"])
builder.add_edge("researcher", "supervisor")
builder.add_edge("coder", "supervisor")

graph = builder.compile()

# Example usage
initial_state = {
    "messages": [
        {
            "role": "user",
            "content": "I need help analyzing some data and creating a visualization.",
        }
    ],
    "next": "supervisor",
}

for output in graph.stream(initial_state):
    print(f"\nStep decision: {output.get('next', 'N/A')}")
    if output.get("messages"):
        print(f"Response: {output['messages'][-1].content[:100]}...")
