from langchain_community.document_loaders import DirectoryLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',
    loader_cls=PyMuPDF4LLMLoader
)

docs = loader.lazy_load()

for document in docs:
    print(document.metadata)