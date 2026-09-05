from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

context="policy says an employee can take 5 days leave a an year"
#question="how many days an employee can take leaves in an year"

#promptstatement = f"Use the following context to answer the question:Context: {context}  Question: {} Answer:",context,question

promptstatement = f"Use the following context to answer the question:Context: {context}  Question:  Answer:",context
    
print(promptstatement)

result = model.invoke(promptstatement)

print(result.content)

#1. Not chainable 2. No validation
#PromptTemplate can raise errors before the LLM is called
# from langchain_core.prompts import PromptTemplate

# prompt = PromptTemplate.from_template(
#     "Explain {topic} in {style} style."
# )

# prompt.invoke({"topic": "Transformers"})
    # This will raise an error:
    # Because {style} is missing.
    # The error happens:
    # Before calling the LLM
    # During prompt formatting
    