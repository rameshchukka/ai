/**
 * Define the configurable parameters for the agent.
 */

import { Annotation } from '@langchain/langgraph';
import { RunnableConfig } from '@langchain/core/runnables';

/**
 * typeof ConfigurationAnnotation.State class for indexing and retrieval operations.
 *
 * @property embeddingModel - The name of the openai embedding model to use.
 * @property retrieverProvider - The vector store provider to use for retrieval.
 * @property filter - Optional filter criteria to limit the items retrieved based on the specified filter type.
 * @property k - The number of results to return from the retriever.
 */

export const BaseConfigurationAnnotation = Annotation.Root({
  /**
   * Name of the openai embedding model to use. Must be a valid embedding model name.
   */
  embeddingModel: Annotation<'text-embedding-3-small'>,

  /**
   * The vector store provider to use for retrieval.
   * Options are 'supabase', 'chroma'.
   */
  retrieverProvider: Annotation<'supabase' | 'chroma'>,

  /**
   * Optional filter criteria to limit the items retrieved.
   * Can be any metadata object that matches document metadata structure.
   */
  filter: Annotation<Record<string, any> | undefined>,

  /**
   * The number of results to return from the retriever.
   */
  k: Annotation<number>,
});

/**
 * Create an typeof BaseConfigurationAnnotation.State instance from a RunnableConfig object.
 *
 * @param config - The configuration object to use.
 * @returns An instance of typeof BaseConfigurationAnnotation.State with the specified configuration.
 */
export function ensureBaseConfiguration(
  config: RunnableConfig
): typeof BaseConfigurationAnnotation.State {
  const configurable = (config?.configurable || {}) as Partial<
    typeof BaseConfigurationAnnotation.State
  >;
  return {
    embeddingModel: configurable.embeddingModel || 'text-embedding-3-small',
    retrieverProvider: configurable.retrieverProvider || 'supabase',
    filter: configurable.filter,
    k: configurable.k || 4,
  };
}
