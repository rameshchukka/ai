from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Optionally check if the key is loaded
#print(os.getenv("GOOGLE_API_KEY"))

embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    #api_key=os.getenv("GOOGLE_API_KEY")  # pass key explicitly
)

vector = embeddings.embed_query("Hello world")
print(vector)
