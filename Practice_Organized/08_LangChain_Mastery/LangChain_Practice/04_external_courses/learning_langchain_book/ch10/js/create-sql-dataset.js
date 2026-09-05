import { Client } from 'langsmith';
const client = new Client();

const exampleInputs = [
  [
    "Which country's customers spent the most? And how much did they spend?",
    'The country whose customers spent the most is the USA, with a total expenditure of $523.06',
  ],
  [
    'What was the most purchased track of 2013?',
    'The most purchased track of 2013 was Hot Girl.',
  ],
  [
    'How many albums does the artist Led Zeppelin have?',
    'Led Zeppelin has 14 albums',
  ],
  [
    "What is the total price for the album 'Big Ones'?",
    'The total price for the album "Big Ones" is 14.85',
  ],
  [
    'Which sales agent made the most in sales in 2009?',
    'Steve Johnson made the most sales in 2009',
  ],
];

const datasetName = 'sql-agent-response';

if (!(await client.hasDataset({ datasetName }))) {
  client.createDataset(datasetName);

  // Prepare inputs, outputs, and metadata for bulk creation
  const inputs = exampleInputs.map(([inputPrompt]) => ({
    question: inputPrompt,
  }));

  const outputs = exampleInputs.map(([, outputAnswer]) => ({
    answer: outputAnswer,
  }));

  await client.createExamples({
    inputs,
    outputs,
    datasetId: dataset.id,
  });
}
