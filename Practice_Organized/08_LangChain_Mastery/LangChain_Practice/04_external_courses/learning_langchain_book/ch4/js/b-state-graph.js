import {
  StateGraph,
  Annotation,
  messagesStateReducer,
  START,
  END,
} from '@langchain/langgraph';
import { ChatOpenAI } from '@langchain/openai';
import { HumanMessage } from '@langchain/core/messages';

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

builder = builder.addNode('chatbot', chatbot);

builder = builder.addEdge(START, 'chatbot').addEdge('chatbot', END);

let graph = builder.compile();

// Run the graph
const input = { messages: [new HumanMessage('hi!')] };
for await (const chunk of await graph.stream(input)) {
  console.log(chunk);
}
