import { VectorStoreRetriever } from '@langchain/core/vectorstores';
import { OpenAIEmbeddings } from '@langchain/openai';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { createClient } from '@supabase/supabase-js';
import { RunnableConfig } from '@langchain/core/runnables';
import { Embeddings } from '@langchain/core/embeddings';
import { ensureBaseConfiguration } from './configuration.js';
import { Chroma } from '@langchain/community/vectorstores/chroma';

export async function makeSupabaseRetriever(
  configuration: ReturnType<typeof ensureBaseConfiguration>,
  embeddingModel: Embeddings
): Promise<VectorStoreRetriever> {
  if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) {
    throw new Error(
      'SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables are not defined'
    );
  }
  const supabaseClient = createClient(
    process.env.SUPABASE_URL ?? '',
    process.env.SUPABASE_SERVICE_ROLE_KEY ?? ''
  );
  const vectorStore = new SupabaseVectorStore(embeddingModel, {
    client: supabaseClient,
    tableName: 'documents',
    queryName: 'match_documents',
  });
  return vectorStore.asRetriever({
    filter: configuration.filter,
    k: configuration.k,
  });
}

export async function makeChromaRetriever(
  configuration: ReturnType<typeof ensureBaseConfiguration>,
  embeddingModel: Embeddings
) {
  const vectorStore = new Chroma(embeddingModel, {
    collectionName: 'documents',
  });
  return vectorStore.asRetriever({
    filter: configuration.filter,
    k: configuration.k,
  });
}

export async function makeRetriever(
  config: RunnableConfig
): Promise<VectorStoreRetriever> {
  const configuration = ensureBaseConfiguration(config);
  const embeddingModel = new OpenAIEmbeddings({
    model: configuration.embeddingModel,
  });
  switch (configuration.retrieverProvider) {
    case 'supabase':
      return makeSupabaseRetriever(configuration, embeddingModel);
    case 'chroma':
      return makeChromaRetriever(configuration, embeddingModel);
    default:
      throw new Error(
        `Unrecognized retrieverProvider in configuration: ${configuration.retrieverProvider}`
      );
  }
}
