import { MemorySaver } from "@langchain/langgraph";

// Assuming graph is already created and configured
const graph = new StateGraph().compile({ checkpointer: new MemorySaver() });

const config = { configurable: { thread_id: "1" } };

const history = await Array.fromAsync(graph.getStateHistory(config));
console.log("History states:", history.length);

// replay a past state
if (history.length >= 3) {
  const result = await graph.invoke(null, history[2].config);
  console.log("Replayed state result:", result);
}
