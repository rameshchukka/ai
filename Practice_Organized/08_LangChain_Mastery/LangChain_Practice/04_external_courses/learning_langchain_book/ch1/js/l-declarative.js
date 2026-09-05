import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { RunnableLambda } from '@langchain/core/runnables';

// the building blocks

const template = ChatPromptTemplate.fromMessages([
  ['system', 'You are a helpful assistant.'],
  ['human', '{question}'],
]);

const model = new ChatOpenAI({
  model: 'gpt-3.5-turbo',
});

// combine them in a function

const chatbot = template.pipe(model);

// use it

const response = await chatbot.invoke({
  question: 'Which model providers offer LLMs?',
});

console.log(response);

//streaming

for await (const part of chatbot.stream({
  question: 'Which model providers offer LLMs?',
})) {
  console.log(part);
}
