import { ChatOpenAI } from "langchain-openai";
import {
  StateGraph,
  Annotation,
  MessagesAnnotation,
  START,
  END,
} from "@langchain/langgraph";
import { z } from "zod";

// Define decision schema
const SupervisorDecision = z.object({
  next: z.enum(["researcher", "coder", "FINISH"]),
});

// Initialize model
const model = new ChatOpenAI({ model: "gpt-4", temperature: 0 });
const modelWithStructuredOutput =
  model.withStructuredOutput(SupervisorDecision);

// Define available agents
const agents = ["researcher", "coder"];

// Define system prompts
const systemPromptPart1 = `You are a supervisor tasked with managing a conversation between the following workers: ${agents.join(
  ", ",
)}. Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. When finished, respond with FINISH.`;

const systemPromptPart2 = `Given the conversation above, who should act next? Or should we FINISH? Select one of: ${agents.join(
  ", ",
)}, FINISH`;

// Define supervisor
const supervisor = async (state) => {
  const messages = [
    { role: "system", content: systemPromptPart1 },
    ...state.messages,
    { role: "system", content: systemPromptPart2 },
  ];

  return await modelWithStructuredOutput.invoke({ messages });
};

// Define state type
const StateAnnotation = Annotation.Root({
  ...MessagesAnnotation.spec,
  next: Annotation("researcher" | "coder" | "FINISH"),
});

// Define agent functions
const researcher = async (state) => {
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a research assistant. Analyze the request and provide relevant information.",
    },
    state.messages[0],
  ]);
  return { messages: [response] };
};

const coder = async (state) => {
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a coding assistant. Implement the requested functionality.",
    },
    state.messages[0],
  ]);
  return { messages: [response] };
};

// Build the graph
const graph = new StateGraph(StateAnnotation)
  .addNode("supervisor", supervisor)
  .addNode("researcher", researcher)
  .addNode("coder", coder)
  .addEdge(START, "supervisor")
  // Route to one of the agents or exit based on the supervisor's decision
  .addConditionalEdges("supervisor", async (state) =>
    state.next === "FINISH" ? END : state.next,
  )
  .addEdge("researcher", "supervisor")
  .addEdge("coder", "supervisor")
  .compile();

// Example usage

const initialState = {
  messages: [
    {
      role: "user",
      content: "I need help analyzing some data and creating a visualization.",
    },
  ],
  next: "supervisor",
};

for await (const output of graph.stream(initialState)) {
  console.log(`\nStep decision: ${output.next || "N/A"}`);
  if (output.messages) {
    console.log(
      `Response: ${output.messages[output.messages.length - 1].content.slice(
        0,
        100,
      )}...`,
    );
  }
}
