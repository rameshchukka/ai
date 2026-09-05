from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)

documents = [
    "I am good at Agentic AI",
    "He is very happy with outcome",
    "She went to meet her friends"
]

result = embedding.embed_documents(documents)

print(str(result))