from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

#pip install BeautifulSoup4
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = PromptTemplate(
    template='Answer the following question \n {question} from the following text - \n {text}',
    input_variables=['question','text']
)

parser = StrOutputParser()

#many websites block scripts without a User-Agent (for security reasons).
os.environ["USER_AGENT"] = "Prudvi-RAG-Loader/0.1"


url = 'https://docs.langchain.com/oss/python/integrations/document_loaders'
loader = WebBaseLoader(url)

docs = loader.load()


chain = prompt | model | parser

print(chain.invoke({'question':'What topics are discussion in this?', 'text':docs[0].page_content}))