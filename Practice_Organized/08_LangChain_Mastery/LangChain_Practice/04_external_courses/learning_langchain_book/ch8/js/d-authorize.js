import { HumanMessage } from "@langchain/core/messages";
import { MemorySaver } from "@langchain/langgraph";

// Assuming graph is already created and configured
const graph = new StateGraph().compile({ checkpointer: new MemorySaver() });

const input = {
  messages: [
    new HumanMessage(
      "How old was the 30th president of the United States when he died?",
    ),
  ],
};

const config = { configurable: { thread_id: "1" } };

const output = await graph.stream(input, {
  ...config,
  interruptBefore: ["tools"],
});

for await (const chunk of output) {
  console.log(chunk); // do something with the output
}
