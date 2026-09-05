from langchain_pymupdf4llm import PyMuPDF4LLMLoader

file_path = r'H:\01_Training\ContentSlides_AgenticAI\Code\LangChain\06_RAG\DocumentLoader\ERP-2008-chapter4.pdf'
loader = PyMuPDF4LLMLoader(file_path)

docs = loader.load()
print(docs[0])