import {
  HumanMessage,
  SystemMessage,
  AIMessage,
  filterMessages,
} from '@langchain/core/messages';

const messages = [
  new SystemMessage({ content: 'you are a good assistant', id: '1' }),
  new HumanMessage({ content: 'example input', id: '2', name: 'example_user' }),
  new AIMessage({
    content: 'example output',
    id: '3',
    name: 'example_assistant',
  }),
  new HumanMessage({ content: 'real input', id: '4', name: 'bob' }),
  new AIMessage({ content: 'real output', id: '5', name: 'alice' }),
];

// Filter for human messages
const filterByHumanMessages = filterMessages(messages, {
  includeTypes: ['human'],
});
console.log(`Human messages: ${JSON.stringify(filterByHumanMessages)}`);

// Filter to exclude names
const filterByExcludedNames = filterMessages(messages, {
  excludeNames: ['example_user', 'example_assistant'],
});
console.log(
  `\nExcluding example names: ${JSON.stringify(filterByExcludedNames)}`
);

// Filter by types and IDs
const filterByTypesAndIDs = filterMessages(messages, {
  includeTypes: ['human', 'ai'],
  excludeIds: ['3'],
});
console.log(
  `\nFiltered by types and IDs: ${JSON.stringify(filterByTypesAndIDs)}`
);
