from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = PromptTemplate(
    template='Write a summary for the following topic - \n {story}',
    input_variables=['story']
)

parser = StrOutputParser()

loader = TextLoader('movie.txt', encoding='utf-8')

docs = loader.load()

# print(type(docs))

# print(len(docs))

# print(docs[0].page_content)

# print(docs[0].metadata)

chain = prompt | model | parser

print(chain.invoke({'story':docs[0].page_content}))

