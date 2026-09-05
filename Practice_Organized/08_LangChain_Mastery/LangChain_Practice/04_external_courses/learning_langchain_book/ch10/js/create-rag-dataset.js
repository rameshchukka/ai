import { Client } from 'langsmith';
const client = new Client();

const exampleInputs = [
  [
    'Which companies are highlighted as top LangGraph agent adopters in 2024?',
    'The top adopters include Uber (code migration tools), AppFolio (property management copilot), LinkedIn (SQL Bot), Elastic (AI assistant), and Replit (multi-agent development platform) :cite[3].',
  ],
  [
    "How did AppFolio's AI copilot impact property managers?",
    "AppFolio's Realm-X AI copilot saved property managers over 10 hours per week by automating queries, bulk actions, and scheduling :cite[3].",
  ],
  [
    'What infrastructure trends dominated LLM usage in 2024?',
    'OpenAI remained the top LLM provider (6x more usage than Ollama), while open-source models via Ollama and Groq surged. Chroma and FAISS led vector stores, with MongoDB and Elastic gaining traction :cite[2]:cite[5].',
  ],
  [
    'How did LangGraph improve agent workflows compared to 2023?',
    'LangGraph usage grew to 43% of LangSmith organizations, with 21.9% of traces involving tool calls (up from 0.5% in 2023), enabling complex multi-step tasks like database writes :cite[2]:cite[7].',
  ],
  [
    "What distinguishes Replit's LangGraph implementation?",
    "Replit's agent emphasizes human-in-the-loop validation and a multi-agent architecture for code generation, combining autonomy with controlled outputs :cite[3].",
  ],
];

const datasetName = 'langchain-blogs-qa';

// Create dataset
const dataset = await client.createDataset(datasetName, {
  description: 'Langchain blogs QA.',
});

// Prepare inputs, outputs, and metadata for bulk creation
const inputs = exampleInputs.map(([inputPrompt]) => ({
  question: inputPrompt,
}));

const outputs = exampleInputs.map(([, outputAnswer]) => ({
  answer: outputAnswer,
}));

const metadata = exampleInputs.map(() => ({ source: 'LangChain Blog' }));

// Use the bulk createExamples method
await client.createExamples({
  inputs,
  outputs,
  metadata,
  datasetId: dataset.id,
});

console.log(
  `Dataset created in langsmith with ID: ${dataset.id}\n Navigate to ${dataset.url}.`
);
