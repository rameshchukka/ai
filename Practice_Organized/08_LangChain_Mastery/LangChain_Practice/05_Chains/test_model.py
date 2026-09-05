from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model

load_dotenv()

# chat_model = ChatGoogleGenerativeAI(model = os.getenv("model_name"))

model = init_chat_model("gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

model = init_chat_model(os.getenv("model_name"), api_key=os.getenv("GEMINI_API_KEY"))