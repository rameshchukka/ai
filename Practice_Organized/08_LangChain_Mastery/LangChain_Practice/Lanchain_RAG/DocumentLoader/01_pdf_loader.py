from langchain_community.document_loaders import PyPDFLoader
#pip install pypdf
loader = PyPDFLoader(r'H:\01_Training\ContentSlides_AgenticAI\Code\LangChain\06_RAG\DocumentLoader\ERP-2008-chapter4.pdf')

docs = loader.load()

print(len(docs))

print(docs[0].page_content)
print(docs[1].metadata)