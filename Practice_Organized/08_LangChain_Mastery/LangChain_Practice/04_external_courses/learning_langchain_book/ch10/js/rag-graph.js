import { Annotation, StateGraph } from '@langchain/langgraph';
import { CheerioWebBaseLoader } from '@langchain/community/document_loaders/web/cheerio';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { MemoryVectorStore } from 'langchain/vectorstores/memory';
import { ChatOpenAI, OpenAIEmbeddings } from '@langchain/openai';
import * as hub from 'langchain/hub';
import { StringOutputParser } from '@langchain/core/output_parsers';

const GraphState = Annotation.Root({
  question: Annotation(),
  scrapedDocuments: Annotation(),
  vectorstore: Annotation(),
  answer: Annotation(),
});

const scrapeBlogPosts = async (state) => {
  const urls = [
    'https://blog.langchain.dev/top-5-langgraph-agents-in-production-2024/',
    'https://blog.langchain.dev/langchain-state-of-ai-2024/',
    'https://blog.langchain.dev/introducing-ambient-agents/',
  ];

  const loadDocs = async (urls) => {
    const docs = [];
    for (const url of urls) {
      const loader = new CheerioWebBaseLoader(url);
      const loadedDocs = await loader.load();
      docs.push(...loadedDocs);
    }
    return docs;
  };

  const scrapedDocuments = await loadDocs(urls);

  return { scrapedDocuments };
};

const indexing = async (state) => {
  const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 0,
  });

  const docSplits = await textSplitter.splitDocuments(state.scrapedDocuments);

  const vectorstore = new MemoryVectorStore(new OpenAIEmbeddings());

  await vectorstore.addDocuments(docSplits);

  console.log('vectorstore: ', vectorstore);

  return { vectorstore };
};

const retrieveAndGenerate = async (state) => {
  const { question, vectorstore } = state;

  const retriever = vectorstore.asRetriever();

  const prompt = await hub.pull('rlm/rag-prompt');

  const llm = new ChatOpenAI({ model: 'gpt-3.5-turbo', temperature: 0 });

  const docs = await retriever.invoke(question);

  const chain = prompt.pipe(llm).pipe(new StringOutputParser());

  const answer = await chain.invoke({ context: docs, question });

  console.log('answer: ', answer);

  return { answer };
};

const workflow = new StateGraph(GraphState)
  .addNode('retrieve_and_generate', retrieveAndGenerate)
  .addNode('scrape_blog_posts', scrapeBlogPosts)
  .addNode('indexing', indexing)
  .addEdge('__start__', 'scrape_blog_posts')
  .addEdge('scrape_blog_posts', 'indexing')
  .addEdge('indexing', 'retrieve_and_generate')
  .addEdge('retrieve_and_generate', '__end__');

const graph = workflow.compile();

await graph.invoke({ question: 'What are ambient agents?' });
