import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { evaluate } from 'langsmith/evaluation';
import { traceable } from 'langsmith/traceable';
import { graph } from './rag-graph.js';
import { z } from 'zod';

const defaultDataset = 'langchain-blogs-qa';

const experimentPrefix = 'langchain-blogs-qa-evals';

const llm = new ChatOpenAI({ model: 'gpt-4o', temperature: 0 });

const EVALUATION_PROMPT = `You are a teacher grading a quiz.

You will be given a QUESTION, the GROUND TRUTH (correct) RESPONSE, and the STUDENT RESPONSE.

Here is the grade criteria to follow:
(1) Grade the student responses based ONLY on their factual accuracy relative to the ground truth answer.
(2) Ensure that the student response does not contain any conflicting statements.
(3) It is OK if the student response contains more information than the ground truth response, as long as it is factually accurate relative to the  ground truth response.

Correctness:
True means that the student's response meets all of the criteria.
False means that the student's response does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct.`;

const userPrompt = `QUESTION: {question}
GROUND TRUTH RESPONSE: {reference}
STUDENT RESPONSE: {answer}`;

const prompt = ChatPromptTemplate.fromMessages([
  ['system', EVALUATION_PROMPT],
  ['user', userPrompt],
]);

// LLM-as-judge output schema

const grade = z
  .object({
    reasoning: z
      .string()
      .describe(
        'Explain your reasoning for whether the actual response is correct or not.'
      ),
    isCorrect: z
      .boolean()
      .describe(
        'True if the student response is mostly or exactly correct, otherwise False.'
      ),
  })
  .describe(
    'Compare the expected and actual answers and grade the actual answer.'
  );

const graderLlm = prompt.pipe(llm.withStructuredOutput(grade));

const evaluateAgent = async (run, example) => {
  const question = run.inputs.question;
  const answer = run.outputs.answer;
  const reference = example.outputs.answer;

  const grade = await graderLlm.invoke({ question, reference, answer });
  const isCorrect = grade.isCorrect;

  return { key: 'correct', score: Number(isCorrect) };
};

const runGraph = traceable(async (inputs) => {
  const answer = await graph.invoke({ question: inputs.question });
  return { answer: answer.answer };
});

await evaluate((inputs) => runGraph(inputs), {
  data: defaultDataset,
  evaluators: [evaluateAgent],
  experimentPrefix,
  maxConcurrency: 4,
});
