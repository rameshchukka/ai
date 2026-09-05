import { MemorySaver } from "@langchain/langgraph";

// Assuming graph is already created and configured
const graph = new StateGraph().compile({ checkpointer: new MemorySaver() });

const config = { configurable: { thread_id: "1" } };

const output = await graph.stream(null, {
  ...config,
  interruptBefore: ["tools"],
});

for await (const chunk of output) {
  console.log(chunk); // do something with the output
}
