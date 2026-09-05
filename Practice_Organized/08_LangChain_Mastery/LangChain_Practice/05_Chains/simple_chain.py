from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt_template = PromptTemplate(
    template='Generate 5 interesting facts about {topic}',
    input_variables=['topic']
)

#****************************************************

prompt = prompt_template.invoke({'topic':'cricket'})

print(prompt)

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

result = model.invoke(prompt)

print(result.content)

#*****************************************************

# reslut = prompt_template | model.invoke({'topic':'cricket'})

# print(reslut.content)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'topic':'cricket'})

print(result)

# #pip install grandalf
# chain.get_graph().print_ascii()