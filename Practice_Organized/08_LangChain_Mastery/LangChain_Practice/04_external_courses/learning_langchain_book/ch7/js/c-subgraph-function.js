import { StateGraph, START, Annotation } from '@langchain/langgraph';

const StateAnnotation = Annotation.Root({
  foo: Annotation(),
});

const SubgraphStateAnnotation = Annotation.Root({
  // note that none of these keys are shared with the parent graph state
  bar: Annotation(),
  baz: Annotation(),
});

// Define subgraph
const subgraphNode = async (state) => {
  return { bar: state.bar + 'baz' };
};

const subgraph = new StateGraph(SubgraphStateAnnotation)
  .addNode('subgraph', subgraphNode)
  .addEdge(START, 'subgraph')
  // Additional subgraph setup would go here
  .compile();

// Define parent graph
const subgraphWrapperNode = async (state) => {
  // transform the state to the subgraph state
  const response = await subgraph.invoke({
    bar: state.foo,
  });
  // transform response back to the parent state
  return {
    foo: response.bar,
  };
};

const parentGraph = new StateGraph(StateAnnotation)
  .addNode('subgraph', subgraphWrapperNode)
  .addEdge(START, 'subgraph')
  // Additional parent graph setup would go here
  .compile();

// Example usage

const initialState = { foo: 'hello' };
const result = await parentGraph.invoke(initialState);
console.log(`Result: ${JSON.stringify(result)}`); // Should transform foo->bar, append "baz", then transform bar->foo
