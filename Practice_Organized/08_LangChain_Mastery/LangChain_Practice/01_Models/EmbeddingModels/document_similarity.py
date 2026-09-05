from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)

documents= [
    "Mathematics is a subject focused on numbers, algebra, geometry, and problem-solving skills.",
    "Physics explores the fundamental laws of nature, motion, energy, and the behavior of matter.",
    "Chemistry studies substances, their reactions, and how matter interacts at a molecular level.",
    "Biology examines living organisms, their structure, function, growth, and evolution.",
    "History looks at past events, civilizations, cultures, and how they shape the modern world.",
    "Geography studies the Earth's physical features, climate, resources, and human-environment interaction.",
    "English enhances reading, writing, comprehension, and communication skills in language arts.",
    "Computer Science focuses on programming, algorithms, data structures, and digital problem-solving.",
    "Economics analyzes production, consumption, distribution of resources, and financial systems.",
    "Civics teaches about government, laws, citizenship, and responsibilities in society."
]
query = 'tell me about Economics'

doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]

index, score = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]

print(query)
print(documents[index])
print("similarity score is:", score)




