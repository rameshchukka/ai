import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';
import { CheerioWebBaseLoader } from '@langchain/community/document_loaders/web/cheerio';
import { InMemoryVectorStore } from '@langchain/community/vectorstores/in_memory';
import { OpenAIEmbeddings } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { z } from 'zod';
import { ChatOpenAI } from '@langchain/openai';

const urls = [
  'https://blog.langchain.dev/top-5-langgraph-agents-in-production-2024/',
  'https://blog.langchain.dev/langchain-state-of-ai-2024/',
  'https://blog.langchain.dev/introducing-ambient-agents/',
];

// Load documents from URLs
const loadDocs = async (urls) => {
  const docs = [];
  for (const url of urls) {
    const loader = new CheerioWebBaseLoader(url);
    const loadedDocs = await loader.load();
    docs.push(...loadedDocs);
  }
  return docs;
};

const docsList = await loadDocs(urls);

// Initialize the text splitter
const textSplitter = new RecursiveCharacterTextSplitter({
  chunkSize: 250,
  chunkOverlap: 0,
});

// Split the documents into smaller chunks
const docSplits = textSplitter.splitDocuments(docsList);

// Add to vector database
const vectorstore = await InMemoryVectorStore.fromDocuments(
  docSplits,
  new OpenAIEmbeddings()
);

const retriever = vectorstore.asRetriever(); // The `retriever` object can now be used for querying

const question = 'What are 2 LangGraph agents used in production in 2024?';

const docs = retriever.invoke(question);

console.log('Retrieved documents: \n', docs[0].page_content);

// Define the schema using Zod
const GradeDocumentsSchema = z.object({
  binary_score: z
    .string()
    .describe("Documents are relevant to the question, 'yes' or 'no'"),
});

// Initialize LLM with structured output using Zod schema
const llm = new ChatOpenAI({ model: 'gpt-3.5-turbo', temperature: 0 });
const structuredLLMGrader = llm.withStructuredOutput(GradeDocumentsSchema);

// System and prompt template
const systemMessage = `You are a grader assessing relevance of a retrieved document to a user question. If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.`;
const gradePrompt = ChatPromptTemplate.fromMessages([
  { role: 'system', content: systemMessage },
  {
    role: 'human',
    content:
      'Retrieved document: \n\n {document} \n\n User question: {question}',
  },
]);

// Combine prompt with the structured output
const retrievalGrader = gradePrompt.pipe(structuredLLMGrader);

// Grade retrieved documents
const results = await retrievalGrader.invoke({
  question,
  document: docs[0].page_content,
});

console.log('\n\nGrading results: \n', results);
