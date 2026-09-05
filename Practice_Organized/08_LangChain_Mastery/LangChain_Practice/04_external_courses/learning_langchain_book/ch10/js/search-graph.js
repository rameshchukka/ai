import { Annotation, StateGraph, START, END } from '@langchain/langgraph';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { ChatOpenAI } from '@langchain/openai';
import { DuckDuckGoSearch } from '@langchain/community/tools/duckduckgo_search';
import * as hub from 'langchain/hub';
import { retriever, retrievalGrader } from './retrieve-and-grade.js';
import { Document } from '@langchain/core/documents';

// LLM setup
const prompt = await hub.pull('rlm/rag-prompt');
const llm = new ChatOpenAI({ modelName: 'gpt-4', temperature: 0 }); // Fixed model name
const ragChain = prompt.pipe(llm).pipe(new StringOutputParser());
const webSearchTool = new DuckDuckGoSearch();
// Question rewriting prompt
const rewritePrompt = ChatPromptTemplate.fromMessages([
  [
    'system',
    `You are a question re-writer that converts an input question to a better version that is optimized 
     for web search. Look at the input and try to reason about the underlying semantic intent / meaning.`,
  ],
  [
    'human',
    'Here is the initial question: \n\n {question} \n Formulate an improved question.',
  ],
]);

const questionRewriter = rewritePrompt.pipe(llm).pipe(new StringOutputParser());

// Create the graph state
const GraphState = Annotation.Root({
  question: Annotation(),
  generation: Annotation(),
  webSearch: Annotation(),
  documents: Annotation({
    reducer: (currentState, updateValue) => currentState.concat(updateValue),
    default: () => [],
  }),
});

// Node functions
const retrieve = async (state) => {
  const documents = await retriever.invoke(state.question);
  return { question: state.question, documents };
};

const generate = async (state) => {
  const { question, documents } = state;
  const context = documents.map((doc) => doc.pageContent).join('\n');
  const generation = await ragChain.invoke({ context, question });
  console.log('Final answer:', generation);
  return { documents, question, generation };
};

const gradeDocuments = async (state) => {
  const { question, documents } = state;
  const filteredDocs = [];
  let webSearch = 'No';

  for (const doc of documents) {
    try {
      const score = await retrievalGrader.invoke({
        question: question,
        document: doc.pageContent,
      });

      if (score.binary_score === 'yes') {
        console.log('---GRADE: DOCUMENT RELEVANT---');
        filteredDocs.push(doc);
      } else {
        console.log('---GRADE: DOCUMENT NOT RELEVANT---');
        webSearch = 'Yes';
      }
    } catch (error) {
      console.error('Error grading document:', error);
      webSearch = 'Yes';
    }
  }

  return {
    documents: filteredDocs,
    question,
    webSearch,
  };
};

const transformQuery = async (state) => {
  const betterQuestion = await questionRewriter.invoke({
    question: state.question,
  });
  console.log('Transformed question:', betterQuestion);
  return { documents: state.documents, question: betterQuestion };
};

const webSearch = async (state) => {
  console.log('---WEB SEARCH---');
  const webResult = await webSearchTool.invoke(state.question);
  const webResultsDocument = new Document({ pageContent: webResult });

  // Fixed document concatenation
  const updatedDocuments = [...state.documents, webResultsDocument];

  return { documents: updatedDocuments, question: state.question };
};

// Routing function
const generateRoute = (state) => {
  return state.webSearch === 'Yes' ? 'transform_query' : 'generate';
};

// Create and compile the graph
const workflow = new StateGraph(GraphState)
  .addNode('retrieve', retrieve)
  .addNode('grade_documents', gradeDocuments)
  .addNode('transform_query', transformQuery)
  .addNode('generate', generate)
  .addNode('web_search_node', webSearch)
  .addEdge(START, 'retrieve')
  .addEdge('retrieve', 'grade_documents')
  .addConditionalEdges('grade_documents', generateRoute)
  .addEdge('transform_query', 'web_search_node')
  .addEdge('web_search_node', 'generate')
  .addEdge('generate', END);

const graph = workflow.compile();

const result = await graph.invoke({
  question: 'What are the Top 5 LangGraph Agents in Production 2024?',
});

console.log(result);
