import { Annotation } from '@langchain/langgraph';
import { RunnableConfig } from '@langchain/core/runnables';

// This path points to the directory containing the documents to index.
const DEFAULT_DOCS_PATH = 'src/sample_docs.json';

/**
 * The configuration for the indexing process.
 */
export const IndexConfigurationAnnotation = Annotation.Root({
  /**
   * Path to folder containing default documents to index.
   */
  docsPath: Annotation<string>,

  /**
   * Name of the openai embedding model to use. Must be a valid embedding model name.
   */
  embeddingModel: Annotation<'text-embedding-3-small'>,

  /**
   * The vector store provider to store the embeddings.
   * Options are 'supabase', 'chroma'.
   */
  retrieverProvider: Annotation<'supabase' | 'chroma'>,

  /**
   * Whether to index sample documents specified in the docsPath.
   */
  useSampleDocs: Annotation<boolean>,
});

/**
 * Create an typeof IndexConfigurationAnnotation.State instance from a RunnableConfig object.
 *
 * @param config - The configuration object to use.
 * @returns An instance of typeof IndexConfigurationAnnotation.State with the specified configuration.
 */
export function ensureIndexConfiguration(
  config: RunnableConfig
): typeof IndexConfigurationAnnotation.State {
  const configurable = (config?.configurable || {}) as Partial<
    typeof IndexConfigurationAnnotation.State
  >;
  return {
    docsPath: configurable.docsPath || DEFAULT_DOCS_PATH,
    embeddingModel: configurable.embeddingModel || 'text-embedding-3-small',
    retrieverProvider: configurable.retrieverProvider || 'supabase',
    useSampleDocs: configurable.useSampleDocs || false,
  };
}
