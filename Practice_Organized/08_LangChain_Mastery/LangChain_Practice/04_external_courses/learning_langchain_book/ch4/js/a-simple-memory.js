import { ChatPromptTemplate } from '@langchain/core/prompts';
import { ChatOpenAI } from '@langchain/openai';

const prompt = ChatPromptTemplate.fromMessages([
  [
    'system',
    'You are a helpful assistant. Answer all questions to the best of your ability.',
  ],
  ['placeholder', '{messages}'],
]);
const model = new ChatOpenAI();
const chain = prompt.pipe(model);

const response = await chain.invoke({
  messages: [
    [
      'human',
      'Translate this sentence from English to French: I love programming.',
    ],
    ['ai', "J'adore programmer."],
    ['human', 'What did you just say?'],
  ],
});

console.log(response.content);
