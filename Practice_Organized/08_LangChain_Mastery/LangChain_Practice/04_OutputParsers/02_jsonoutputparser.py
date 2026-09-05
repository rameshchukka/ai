from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

# Define the model
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

#json will provide the JSON object but no specific schema so will use structuredOutputParser
parser = JsonOutputParser()

print(parser.get_format_instructions())

template = PromptTemplate(
    template='Give me 5 facts about {topic} \n {str_json_str}',
    input_variables=['topic'],
    partial_variables={'str_json_str': parser.get_format_instructions()}
)

template = PromptTemplate(
    template='Give me 5 facts about {topic} \n {str_json_str}',
    input_variables=['topic'],
    partial_variables={'str_json_str': parser.get_format_instructions()}
)

# below 2 lines are just to print prompt
# prompt = template.invoke({'topic':'black hole'})
# print(prompt)

chain = template | model | parser

result = chain.invoke({'topic':'black hole'})

print(result)

