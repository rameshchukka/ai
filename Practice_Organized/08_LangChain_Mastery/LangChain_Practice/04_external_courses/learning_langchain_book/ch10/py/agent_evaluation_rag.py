from typing import Optional

from langchain_openai import ChatOpenAI
from langsmith import Client, evaluate, aevaluate
from langsmith.evaluation import EvaluationResults
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict
from rag_graph import graph

client = Client()

DEFAULT_DATASET_NAME = "langchain-blogs-qa"

llm = ChatOpenAI(model="gpt-4o", temperature=0)

EVALUATION_PROMPT = f"""You are a teacher grading a quiz.

You will be given a QUESTION, the GROUND TRUTH (correct) RESPONSE, and the STUDENT RESPONSE.

Here is the grade criteria to follow:
(1) Grade the student responses based ONLY on their factual accuracy relative to the ground truth answer.
(2) Ensure that the student response does not contain any conflicting statements.
(3) It is OK if the student response contains more information than the ground truth response, as long as it is factually accurate relative to the  ground truth response.

Correctness:
True means that the student's response meets all of the criteria.
False means that the student's response does not meet all of the criteria.

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct."""

# LLM-as-judge output schema


class Grade(TypedDict):
    """Compare the expected and actual answers and grade the actual answer."""
    reasoning: Annotated[str, ...,
                         "Explain your reasoning for whether the actual response is correct or not."]
    is_correct: Annotated[bool, ...,
                          "True if the student response is mostly or exactly correct, otherwise False."]


grader_llm = llm.with_structured_output(Grade)
# PUBLIC API


def transform_dataset_inputs(inputs: dict) -> dict:
    """Transform LangSmith dataset inputs to match the agent's input schema before invoking the agent."""
    # see the `Example input` in the README for reference on what `inputs` dict should look like
    # the dataset inputs already match the agent's input schema, but you can add any additional processing here
    return inputs


def transform_agent_outputs(outputs: dict) -> dict:
    """Transform agent outputs to match the LangSmith dataset output schema."""
    # see the `Example output` in the README for reference on what the output should look like
    return {"info": outputs["info"]}

# Evaluator function


async def evaluate_agent(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    """Evaluate if the final response is equivalent to reference response."""

    # Note that we assume the outputs has a 'response' dictionary. We'll need to make sure
    # that the target function we define includes this key.
    user = f"""QUESTION: {inputs['question']}
    GROUND TRUTH RESPONSE: {reference_outputs['answer']}
    STUDENT RESPONSE: {outputs['answer']}"""

    grade = await grader_llm.ainvoke([{"role": "system", "content": EVALUATION_PROMPT}, {"role": "user", "content": user}])
    is_correct = grade["is_correct"]
    return is_correct


# Target function
async def run_graph(inputs: dict) -> dict:
    """Run graph and track the trajectory it takes along with the final response."""
    result = await graph.ainvoke({
        "question": inputs["question"]
    })
    return {"answer": result["answer"].content}

# run evaluation


async def run_eval(
    dataset_name: str,
    experiment_prefix: Optional[str] = None,
) -> EvaluationResults:
    dataset = client.read_dataset(dataset_name=dataset_name)
    results = await aevaluate(
        run_graph,
        data=dataset,
        evaluators=[evaluate_agent],
        experiment_prefix=experiment_prefix,
    )
    return results


async def main():
    experiment_results = await run_eval(dataset_name=DEFAULT_DATASET_NAME,
                                        experiment_prefix="langchain-blogs-qa-evals")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
