# from langchain_community.document_loaders import BrowserbaseLoader

# loader = BrowserbaseLoader(
#     urls=["https://docs.langchain.com/oss/python/integrations/document_loaders/browserbase"],
#     text_content=False,
# )

# docs = loader.load()
# print(docs[0].page_content[:61])


from langchain_docling.loader import DoclingLoader

FILE_PATH = "https://arxiv.org/pdf/2408.09869"

loader = DoclingLoader(file_path=FILE_PATH)