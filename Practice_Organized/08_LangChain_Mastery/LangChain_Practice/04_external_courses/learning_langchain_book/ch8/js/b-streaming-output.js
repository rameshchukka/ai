import { HumanMessage } from "@langchain/core/messages";

// Assuming graph is already created and configured
const graph = new StateGraph().compile();

const input = {
  messages: [
    new HumanMessage(
      "How old was the 30th president of the United States when he died?",
    ),
  ],
};

const config = { configurable: { thread_id: "1" } };

// Assuming graph is already created and configured
const output = await graph.stream(input, config);

for await (const chunk of output) {
  console.log(chunk);
}
