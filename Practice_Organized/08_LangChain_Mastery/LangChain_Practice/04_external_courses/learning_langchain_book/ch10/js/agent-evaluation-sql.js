import { ChatOpenAI } from '@langchain/openai';
import { graph } from './agent-sql-graph.js';
import crypto from 'crypto';
import * as hub from 'langchain/hub';
import { evaluate } from 'langsmith/evaluation';
import { traceable } from 'langsmith/traceable';
import { z } from 'zod';

const thread_id = crypto.randomUUID();
const config = {
  configurable: {
    thread_id: thread_id,
  },
};

const llm = new ChatOpenAI({ model: 'gpt-4o-mini', temperature: 0 });

const predictSQLAgentAnswer = traceable(async (example) => {
  const messages = await graph.invoke(
    { messages: ['user', example.input] },
    config
  );
  return { response: messages.messages[messages.messages.length - 1].content };
});

const gradePromptAnswerAccuracy = await hub.pull(
  'langchain-ai/rag-answer-vs-reference'
);

const grade = z.object({
  score: z.number(),
});

const answerEvaluator = async (run, example) => {
  const input_question = example.inputs['input'];
  const reference = example.outputs['output'];
  const prediction = run.outputs['response'];

  const grader = gradePromptAnswerAccuracy.pipe(llm);
  const score = await grader.invoke({
    question: input_question,
    correct_answer: reference,
    student_answer: prediction,
  });
  return { key: 'answer_v_reference_score', score: score.Score };
};

const datasetName = 'sql-agent-response';
const experimentPrefix = 'sql-agent-gpt4o';

const experimentResults = await evaluate(
  (inputs) => predictSQLAgentAnswer(inputs),
  {
    data: datasetName,
    evaluators: [answerEvaluator],
    experimentPrefix,
    maxConcurrency: 4,
  }
);

// Single tool evaluation
const predictAssistant = traceable(async (example) => {
  const result = await graph.invoke(
    { messages: [['user', example.input]] },
    config
  );
  return { response: result };
});

const checkSpecificToolCall = async (run, example) => {
  const response = run.outputs['response'];
  const messages = response.messages;

  let firstToolCall = null;
  for (const message of messages) {
    if (message.tool_calls?.length > 0) {
      // Get the name of the first tool call in the message
      firstToolCall = message.tool_calls[0].name;
      break;
    }
  }

  const expected_tool_call = 'list-tables-sql';
  const score = firstToolCall === expected_tool_call ? 1 : 0;

  return {
    key: 'single_tool_call',
    score: score,
  };
};

const singleToolCallResults = await evaluate(
  (inputs) => predictAssistant(inputs),
  {
    data: datasetName,
    evaluators: [checkSpecificToolCall],
    experimentPrefix: `${experimentPrefix}-single-tool`,
    maxConcurrency: 4,
  }
);

const EXPECTED_TOOLS = {
  LIST_TABLES: 'list-tables-sql',
  SCHEMA: 'info-sql',
  QUERY_CHECK: 'query-checker',
  QUERY_EXEC: 'query-sql',
  RESULT_CHECK: 'checkResult',
};

const containsAllToolCallsAnyOrder = async ({ run, example }) => {
  const expected = [
    EXPECTED_TOOLS.LIST_TABLES,
    EXPECTED_TOOLS.SCHEMA,
    EXPECTED_TOOLS.QUERY_CHECK,
    EXPECTED_TOOLS.QUERY_EXEC,
  ];

  const messages = run.outputs?.response?.messages || [];
  const toolCalls = Array.from(
    new Set(
      messages.flatMap(
        (m) => m.tool_calls?.map((tc) => tc.name) || m.name || []
      )
    )
  );

  const score = expected.every((tool) => toolCalls.includes(tool)) ? 1 : 0;
  return { key: 'multi_tool_call_any_order', score };
};

const containsAllToolCallsInOrder = async ({ run, example }) => {
  const expectedSequence = [
    EXPECTED_TOOLS.LIST_TABLES,
    EXPECTED_TOOLS.SCHEMA,
    EXPECTED_TOOLS.QUERY_CHECK,
    EXPECTED_TOOLS.QUERY_EXEC,
  ];

  const messages = run.outputs?.response?.messages || [];
  const toolCalls = messages.flatMap(
    (m) => m.tool_calls?.map((tc) => tc.name) || m.name || []
  );

  let seqIndex = 0;
  for (const call of toolCalls) {
    if (call === expectedSequence[seqIndex]) {
      seqIndex++;
      if (seqIndex === expectedSequence.length) break;
    }
  }

  return {
    key: 'multi_tool_call_in_order',
    score: seqIndex === expectedSequence.length ? 1 : 0,
  };
};

const containsAllToolCallsExactOrder = async ({ run, example }) => {
  const expectedSequence = [
    EXPECTED_TOOLS.LIST_TABLES,
    EXPECTED_TOOLS.SCHEMA,
    EXPECTED_TOOLS.QUERY_CHECK,
    EXPECTED_TOOLS.QUERY_EXEC,
  ];

  const messages = run.outputs?.response?.messages || [];
  const toolCalls = messages.flatMap(
    (m) => m.tool_calls?.map((tc) => tc.name) || m.name || []
  );

  // Find the first occurrence sequence
  const firstOccurrences = [];
  for (const call of toolCalls) {
    if (call === expectedSequence[firstOccurrences.length]) {
      firstOccurrences.push(call);
      if (firstOccurrences.length === expectedSequence.length) break;
    }
  }

  const score =
    JSON.stringify(firstOccurrences) === JSON.stringify(expectedSequence)
      ? 1
      : 0;
  return { key: 'multi_tool_call_exact_order', score };
};

// Prediction functions for different evaluation types
const predictSqlAgentMessages = traceable(async (example) => {
  const result = await graph.invoke(
    { messages: [['user', example.input]] },
    config
  );
  return { response: result };
});

// Trajectory Evaluation Execution
const trajectoryResults = await evaluate(
  (inputs) => predictSqlAgentMessages(inputs),
  {
    data: datasetName,
    evaluators: [
      containsAllToolCallsAnyOrder,
      containsAllToolCallsInOrder,
      containsAllToolCallsExactOrder,
    ],
    experimentPrefix: `${experimentPrefix}-full-trajectory`,
    maxConcurrency: 4,
  }
);
