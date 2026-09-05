from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt_temp1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt_temp2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

parser = StrOutputParser()

chain = prompt_temp1 | model | parser | prompt_temp2 | model | parser

#chain = prompt_temp1 | model |  prompt_temp2 | model 

result = chain.invoke({'topic': 'Unemployment in India'})

print(result)

chain.get_graph().print_ascii()