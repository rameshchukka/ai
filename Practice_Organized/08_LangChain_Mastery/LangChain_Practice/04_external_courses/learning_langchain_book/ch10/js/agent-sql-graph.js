import { ChatOpenAI } from '@langchain/openai';
import { SqlDatabase } from 'langchain/sql_db';
import { DataSource } from 'typeorm';
import { SqlToolkit } from 'langchain/agents/toolkits/sql';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { z } from 'zod';
import { tool } from '@langchain/core/tools';
import { ToolNode } from '@langchain/langgraph/prebuilt';
import { SqliteSaver } from '@langchain/langgraph-checkpoint-sqlite';
import {
  StateGraph,
  MessagesAnnotation,
  END,
  START,
} from '@langchain/langgraph';
import Database from 'better-sqlite3';

// LLM
const llm = new ChatOpenAI({ model: 'gpt-4o', temperature: 0 });

// SQL toolkit
const datasource = new DataSource({
  type: 'sqlite',
  database: 'Chinook_Sqlite.sqlite',
});

const db = await SqlDatabase.fromDataSourceParams({
  appDataSource: datasource,
});

console.log(db.allTables.map((t) => t.tableName));

const toolkit = new SqlToolkit(db, llm);
const tools = toolkit.getTools();

// Query checking
const queryCheckSystemPrompt = `You are a SQL expert with a strong attention to detail.
Double check the SQLite query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Execute the correct query with the appropriate tool.`;

const queryCheckPrompt = ChatPromptTemplate.fromMessages([
  ['system', queryCheckSystemPrompt],
  ['user', '{query}'],
]);

const queryChain = queryCheckPrompt.pipe(llm);

const checkQueryTool = tool(
  async (input) => {
    const res = await queryChain.invoke(input.query);
    return res.content;
  },
  {
    name: 'checkQuery',
    description:
      'Use this tool to double check if your query is correct before executing it.',
    schema: z.object({
      query: z.string(),
    }),
  }
);

// Query result checking
const queryResultCheckSystemPrompt = `You are grading the result of a SQL query from a DB. 
- Check that the result is not empty.
- If it is empty, instruct the system to re-try!`;

const queryResultCheckPrompt = ChatPromptTemplate.fromMessages([
  ['system', queryResultCheckSystemPrompt],
  ['user', '{query_result}'],
]);

const queryResultChain = queryResultCheckPrompt.pipe(llm);

const checkResultTool = tool(
  async (input) => {
    const res = await queryResultChain.invoke(input.query);
    return res.content;
  },
  {
    name: 'checkResult',
    description:
      'Use this tool to check the query result from the database to confirm it is not empty and is relevant.',
    schema: z.object({
      query_result: z.string(),
    }),
  }
);

tools.push(checkQueryTool, checkResultTool);

// Assistant runnable
const queryGenSystem = `
ROLE:
You are an agent designed to interact with a SQL database. You have access to tools for interacting with the database.
GOAL:
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
INSTRUCTIONS:
- Only use the below tools for the following operations.
- Only use the information returned by the below tools to construct your final answer.
- To start you should ALWAYS look at the tables in the database to see what you can query. Do NOT skip this step.
- Then you should query the schema of the most relevant tables.
- Write your query based upon the schema of the tables. You MUST double check your query before executing it. 
- Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
- You can order the results by a relevant column to return the most interesting examples in the database.
- Never query for all the columns from a specific table, only ask for the relevant columns given the question.
- If you get an error while executing a query, rewrite the query and try again.
- If the query returns a result, use check_result tool to check the query result.
- If the query result result is empty, think about the table schema, rewrite the query, and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
`;

const queryGenPrompt = ChatPromptTemplate.fromMessages([
  ['system', queryGenSystem],
  ['placeholder', '{messages}'],
]);

const modelWithTools = queryGenPrompt.pipe(llm.bindTools(tools));

const handleToolError = async (state) => {
  const { messages } = state;
  const toolsByName = {
    checkQuery: checkQueryTool,
    checkResult: checkResultTool,
  };
  const lastMessage = messages[messages.length - 1];
  const outputMessages = [];
  for (const toolCall of lastMessage.tool_calls) {
    try {
      const toolResult = await toolsByName[toolCall.name].invoke(toolCall);
      outputMessages.push(toolResult);
    } catch (error) {
      // Return the error if the tool call fails
      outputMessages.push(
        new ToolMessage({
          content: error.message,
          name: toolCall.name,
          tool_call_id: toolCall.id,
          additional_kwargs: { error },
        })
      );
    }
  }
  return { messages: outputMessages };
};

const toolNodeForGraph = new ToolNode(tools).withFallbacks([handleToolError]);

const shouldContinue = (state) => {
  const { messages } = state;
  const lastMessage = messages[messages.length - 1];
  if (
    'tool_calls' in lastMessage &&
    Array.isArray(lastMessage.tool_calls) &&
    lastMessage.tool_calls?.length
  ) {
    return 'tools';
  }
  return END;
};

export const callModel = async (state) => {
  const { messages } = state;
  const response = await modelWithTools.invoke({ messages });
  return { messages: response };
};

const builder = new StateGraph(MessagesAnnotation)
  // Define the two nodes we will cycle between
  .addNode('agent', callModel)
  .addNode('tools', toolNodeForGraph)
  .addEdge(START, 'agent')
  .addConditionalEdges('agent', shouldContinue, ['tools', END])
  .addEdge('tools', 'agent');

const memory = new SqliteSaver(new Database(':memory:'));
export const graph = builder.compile({ checkpointer: memory });
