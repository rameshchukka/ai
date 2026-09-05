from agent_sql_graph import builder
from langchain import hub
from langchain_openai import ChatOpenAI
from langsmith.evaluation import evaluate
from langsmith.schemas import Example, Run
from langchain_core.runnables import Runnable
from agent_sql_graph import assistant_runnable
import uuid
_printed = set()
thread_id = str(uuid.uuid4())
experiment_prefix = "sql-agent-gpt4o"
metadata = "chinook-gpt-4o-base-case-agent"
config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}


def predict_sql_agent_answer(example: dict):
    """Use this for answer evaluation"""
    msg = {"messages": ("user", example["input"])}
    messages = graph.invoke(msg, config)
    return {"response": messages['messages'][-1].content}


# Grade prompt
grade_prompt_answer_accuracy = hub.pull(
    "langchain-ai/rag-answer-vs-reference")


def answer_evaluator(run, example) -> dict:
    """
    A simple evaluator for RAG answer accuracy
    """

    # Get question, ground truth answer, chain answer
    input_question = example.inputs["input"]
    reference = example.outputs["output"]
    prediction = run.outputs["response"]

    # LLM grader
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Structured prompt
    answer_grader = grade_prompt_answer_accuracy | llm

    # Run evaluator
    score = answer_grader.invoke({"question": input_question,
                                  "correct_answer": reference,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}


dataset_name = "sql-agent-response"
experiment_results = evaluate(
    predict_sql_agent_answer,
    data=dataset_name,
    evaluators=[answer_evaluator],
    num_repetitions=3,
    experiment_prefix=experiment_prefix,
    metadata={"version": metadata},
)


"""
Single tool evaluation

"""


def predict_assistant(example: dict):
    """Invoke assistant for single tool call evaluation"""
    msg = [("user", example["input"])]
    result = assistant_runnable.invoke({"messages": msg})
    return {"response": result}


def check_specific_tool_call(root_run: Run, example: Example) -> dict:
    """
    Check if the first tool call in the response matches the expected tool call.
    """

    # Exepected tool call
    expected_tool_call = 'sql_db_list_tables'

    # Run
    response = root_run.outputs["response"]

    # Get tool call
    try:
        tool_call = getattr(response, 'tool_calls', [])[0]['name']

    except (IndexError, KeyError):
        tool_call = None

    score = 1 if tool_call == expected_tool_call else 0
    return {"score": score, "key": "single_tool_call"}


experiment_results = evaluate(
    predict_assistant,
    data=dataset_name,
    evaluators=[check_specific_tool_call],
    experiment_prefix=experiment_prefix + "-single-tool",
    num_repetitions=3,
    metadata={"version": metadata},
)


"""
Agent trajectory evaluation
"""


def predict_sql_agent_messages(example: dict):
    """Use this for answer evaluation"""
    msg = {"messages": ("user", example["input"])}
    graph = builder.compile()
    messages = graph.invoke(msg, config)
    return {"response": messages}


def find_tool_calls(messages):
    """  
    Find all tool calls in the messages returned 
    """
    tool_calls = [tc['name'] for m in messages['messages']
                  for tc in getattr(m, 'tool_calls', [])]
    return tool_calls


def contains_all_tool_calls_any_order(root_run: Run, example: Example) -> dict:
    """
    Check if all expected tools are called in any order.
    """
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    messages = root_run.outputs["response"]
    tool_calls = find_tool_calls(messages)
    # Optionally, log the tool calls -
    # print("Here are my tool calls:")
    # print(tool_calls)
    if set(expected) <= set(tool_calls):
        score = 1
    else:
        score = 0
    return {"score": int(score), "key": "multi_tool_call_any_order"}


def contains_all_tool_calls_in_order(root_run: Run, example: Example) -> dict:
    """
    Check if all expected tools are called in exact order.
    """
    messages = root_run.outputs["response"]
    tool_calls = find_tool_calls(messages)
    # Optionally, log the tool calls -
    # print("Here are my tool calls:")
    # print(tool_calls)
    it = iter(tool_calls)
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    if all(elem in it for elem in expected):
        score = 1
    else:
        score = 0
    return {"score": int(score), "key": "multi_tool_call_in_order"}


def contains_all_tool_calls_in_order_exact_match(root_run: Run, example: Example) -> dict:
    """
    Check if all expected tools are called in exact order and without any additional tool calls.
    """
    expected = ['sql_db_list_tables', 'sql_db_schema',
                'sql_db_query_checker', 'sql_db_query', 'check_result']
    messages = root_run.outputs["response"]
    tool_calls = find_tool_calls(messages)
    # Optionally, log the tool calls -
    # print("Here are my tool calls:")
    # print(tool_calls)
    if tool_calls == expected:
        score = 1
    else:
        score = 0

    return {"score": int(score), "key": "multi_tool_call_in_exact_order"}


experiment_results = evaluate(
    predict_sql_agent_messages,
    data=dataset_name,
    evaluators=[contains_all_tool_calls_any_order, contains_all_tool_calls_in_order,
                contains_all_tool_calls_in_order_exact_match],
    experiment_prefix=experiment_prefix + "-trajectory",
    num_repetitions=3,
    metadata={"version": metadata},
)
