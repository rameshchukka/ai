from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

class Person(BaseModel):

    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {pydantic_instruction}',
    input_variables=['place'],
    partial_variables={'pydantic_instruction':parser.get_format_instructions()}
)

# final_prompt = template.invoke({'place':'sri lankan'})

# print(final_prompt)

chain1= template | model | parser

result = chain1.invoke({'place':'sri lankan'})

print(result)

