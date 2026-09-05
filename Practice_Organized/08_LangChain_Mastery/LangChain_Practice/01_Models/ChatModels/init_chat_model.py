# The easiest way to get started with a standalone model in LangChain 
# is to use init_chat_model to initialize one from a chat model provider of your choice 

#init_chat_model() in LangChain is only a factory function that 
# detects the provider from the model name and initializes 
# the correct class instance for you.

#you still need to install the provider package(langchain-google-genai), even if you use init_chat_model().

import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_API_KEY"] = "..."

model = init_chat_model("google_genai:gemini-2.5-flash")

response = model.invoke("Why do parrots talk?")


# model = init_chat_model(
#     "claude-sonnet-4-6",
#     # Kwargs passed to the model:
#     temperature=0.7,
#     timeout=30,
#     max_tokens=1000,
#     max_retries=6,  # Default; increase for unreliable networks
# )