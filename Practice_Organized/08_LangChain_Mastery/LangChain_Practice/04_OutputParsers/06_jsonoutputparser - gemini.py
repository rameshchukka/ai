from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

#json will provide the JSON object but no specific schema so will use structuredOutputParser
parser = JsonOutputParser()

print(parser.get_format_instructions())

# template = PromptTemplate(
#     template='Give me 5 facts about {topic} \n {str_json_str}',
#     input_variables=['topic'],
#     partial_variables={'str_json_str': parser.get_format_instructions()}
# )

template = PromptTemplate(
    template='Give me 5 facts about {topic} \n {str_json_str}',
    input_variables=['topic'],
    partial_variables={'str_json_str': parser.get_format_instructions()}
)

#below 2 lines are just to print prompt
prompt = template.invoke({'topic':'black hole'})
print(prompt)

# chain = template | model | parser

# result = chain.invoke({'topic':'black hole'})

# print(result)

