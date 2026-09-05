import { MemorySaver } from "@langchain/langgraph";

// Assuming graph is already created and configured
const graph = new StateGraph().compile({ checkpointer: new MemorySaver() });

const config = { configurable: { thread_id: "1" } };

const state = await graph.getState(config);
console.log("Current state:", state);

// something you want to add or replace
const update = {};

await graph.updateState(config, update);
console.log("State updated");
