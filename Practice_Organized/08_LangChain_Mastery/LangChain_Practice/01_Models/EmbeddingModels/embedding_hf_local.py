from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

documents = [
    "I am good at Agentic AI",
    "He is very happy with outcome",
    "She went to meet her friends"
]

vector = embedding.embed_documents(documents)

print(str(vector))