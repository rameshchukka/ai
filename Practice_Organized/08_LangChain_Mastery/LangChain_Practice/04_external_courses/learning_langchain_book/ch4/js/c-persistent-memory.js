import {
  StateGraph,
  Annotation,
  messagesStateReducer,
  START,
} from "@langchain/langgraph";
import { ChatOpenAI } from "@langchain/openai";
import { MemorySaver } from "@langchain/langgraph";
import { HumanMessage } from "@langchain/core/messages";

const State = {
  messages: Annotation({
    reducer: messagesStateReducer,
    default: () => [],
  }),
};

let builder = new StateGraph(State);

const model = new ChatOpenAI();

async function chatbot(state) {
  const answer = await model.invoke(state.messages);
  return { messages: answer };
}

builder = builder.addNode("chatbot", chatbot);

builder = builder.addEdge(START, "chatbot").addEdge("chatbot", END);

// Add persistence
const graph = builder.compile({ checkpointer: new MemorySaver() });

// Configure thread
const thread1 = { configurable: { thread_id: "1" } };

// Run with persistence
const result_1 = await graph.invoke(
  {
    messages: [new HumanMessage("hi, my name is Jack!")],
  },
  thread1,
);
console.log(result_1);

const result_2 = await graph.invoke(
  {
    messages: [new HumanMessage("what is my name?")],
  },
  thread1,
);
console.log(result_2);

// Get state
await graph.getState(thread1);
