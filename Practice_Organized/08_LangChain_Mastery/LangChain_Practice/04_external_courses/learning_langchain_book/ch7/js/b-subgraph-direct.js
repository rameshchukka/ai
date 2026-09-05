import { StateGraph, START, Annotation } from '@langchain/langgraph';

const StateAnnotation = Annotation.Root({
  foo: Annotation(), // string type
});

const SubgraphStateAnnotation = Annotation.Root({
  foo: Annotation(), // shared with parent graph state
  bar: Annotation(),
});

// Define subgraph
const subgraphNode = async (state) => {
  // note that this subgraph node can communicate with
  // the parent graph via the shared "foo" key
  return { foo: state.foo + 'bar' };
};

const subgraph = new StateGraph(SubgraphStateAnnotation)
  .addNode('subgraph', subgraphNode)
  .addEdge(START, 'subgraph')
  // Additional subgraph setup would go here
  .compile();

// Define parent graph
const parentGraph = new StateGraph(StateAnnotation)
  .addNode('subgraph', subgraph)
  .addEdge(START, 'subgraph')
  // Additional parent graph setup would go here
  .compile();

// Example usage
const initialState = { foo: 'hello' };
const result = await parentGraph.invoke(initialState);
console.log(`Result: ${JSON.stringify(result)}`); // Should append "bar" to the foo value
