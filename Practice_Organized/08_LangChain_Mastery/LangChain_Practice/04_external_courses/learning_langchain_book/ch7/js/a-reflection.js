import {
  AIMessage,
  SystemMessage,
  HumanMessage,
} from '@langchain/core/messages';
import { ChatOpenAI } from '@langchain/openai';
import {
  StateGraph,
  Annotation,
  messagesStateReducer,
  START,
  END,
} from '@langchain/langgraph';

const model = new ChatOpenAI();

const annotation = Annotation.Root({
  messages: Annotation({ reducer: messagesStateReducer, default: () => [] }),
});

const generatePrompt = new SystemMessage(
  `You are an essay assistant tasked with writing excellent 3-paragraph essays.
Generate the best essay possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempts.`
);

async function generate(state) {
  const answer = await model.invoke([generatePrompt, ...state.messages]);
  return { messages: [answer] };
}

const reflectionPrompt = new SystemMessage(
  `You are a teacher grading an essay submission. Generate critique and recommendations for the user's submission.
Provide detailed recommendations, including requests for length, depth, style, etc.`
);

async function reflect(state) {
  // Invert the messages to get the LLM to reflect on its own output
  const clsMap = {
    ai: HumanMessage,
    human: AIMessage,
  };
  // First message is the original user request. We hold it the same for all nodes
  const translated = [
    reflectionPrompt,
    state.messages[0],
    ...state.messages
      .slice(1)
      .map((msg) => new clsMap[msg._getType()](msg.content)),
  ];
  const answer = await model.invoke(translated);
  // We treat the output of this as human feedback for the generator
  return { messages: [new HumanMessage({ content: answer.content })] };
}

function shouldContinue(state) {
  if (state.messages.length > 6) {
    // End after 3 iterations, each with 2 messages
    return END;
  } else {
    return 'reflect';
  }
}

const builder = new StateGraph(annotation)
  .addNode('generate', generate)
  .addNode('reflect', reflect)
  .addEdge(START, 'generate')
  .addConditionalEdges('generate', shouldContinue)
  .addEdge('reflect', 'generate');

const graph = builder.compile();

// Example usage
const initialState = {
  messages: [
    new HumanMessage(
      "Write an essay about the relevance of 'The Little Prince' today."
    ),
  ],
};

for await (const output of await graph.stream(initialState)) {
  const messageType = output.generate ? 'generate' : 'reflect';
  console.log(
    '\nNew message:',
    output[messageType].messages[
      output[messageType].messages.length - 1
    ].content.slice(0, 100),
    '...'
  );
}
