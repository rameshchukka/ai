from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

chat_model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")


# Create prompts
template1 = PromptTemplate.from_template('Write a detailed report on {topic}')


prompt = template1.invoke({'topic': 'black hole'})
result = chat_model.invoke(prompt)
print(result.content)

strparse = StrOutputParser()
finalresult = strparse.invoke(result.content)
print(finalresult)

# # Create chains
# chain1 = template1 | chat_model

# # Execute # print the output without the StrOutputParser
# report = chain1.invoke({'topic': 'black hole'})
# print("DETAILED REPORT:\n", report)

# # with StrOutputParser so the output is properly formatted
# stroutpars = StrOutputParser()

# chain1 = template1 | chat_model | stroutpars
# report = chain1.invoke({'topic': 'black hole'})
# print("DETAILED REPORT:\n", report)