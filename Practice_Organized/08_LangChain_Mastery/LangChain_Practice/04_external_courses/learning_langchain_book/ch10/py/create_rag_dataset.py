from langsmith import wrappers, Client
from pydantic import BaseModel, Field
from openai import OpenAI

client = Client()
openai_client = wrappers.wrap_openai(OpenAI())

examples = [
    {
        "question": "Which companies are highlighted as top LangGraph agent adopters in 2024?",
        "answer": "The top adopters include Uber (code migration tools), AppFolio (property management copilot), LinkedIn (SQL Bot), Elastic (AI assistant), and Replit (multi-agent development platform) :cite[3]."
    },
    {
        "question": "How did AppFolio's AI copilot impact property managers?",
        "answer": "AppFolio's Realm-X AI copilot saved property managers over 10 hours per week by automating queries, bulk actions, and scheduling :cite[3]."
    },
    {
        "question": "What infrastructure trends dominated LLM usage in 2024?",
        "answer": "OpenAI remained the top LLM provider (6x more usage than Ollama), while open-source models via Ollama and Groq surged. Chroma and FAISS led vector stores, with MongoDB and Elastic gaining traction :cite[2]:cite[5]."
    },
    {
        "question": "How did LangGraph improve agent workflows compared to 2023?",
        "answer": "LangGraph usage grew to 43% of LangSmith organizations, with 21.9% of traces involving tool calls (up from 0.5% in 2023), enabling complex multi-step tasks like database writes :cite[2]:cite[7]."
    },
    {
        "question": "What distinguishes Replit's LangGraph implementation?",
        "answer": "Replit's agent emphasizes human-in-the-loop validation and a multi-agent architecture for code generation, combining autonomy with controlled outputs :cite[3]."
    }
]

inputs = [{"question": example["question"]} for example in examples]
outputs = [{"answer": example["answer"]} for example in examples]

# Programmatically create a dataset in LangSmith
dataset = client.create_dataset(
    dataset_name="langchain-blogs-qa", description="Langchain blogs QA."
)

# Add examples to the dataset
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)

print(
    f"Dataset created in langsmith with ID: {dataset.id}\n Navigate to {dataset.url}.")
