"""
Install the beautifulsoup4 package:

```bash
pip install beautifulsoup4
```
"""

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://www.langchain.com/')
docs = loader.load()

print(docs)
