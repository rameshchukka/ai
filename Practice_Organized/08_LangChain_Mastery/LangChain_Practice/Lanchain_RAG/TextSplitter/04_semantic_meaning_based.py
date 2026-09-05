## if this has to work you must have pip install langchain-text-splitters==0.2.2
## in latest modules SemanticChunker is removed
from langchain_text_splitters.semantic import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
text_splitter = SemanticChunker(
    embeddings, 
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=1
)

sample = """
Farmers were working hard in the fields, preparing the soil and planting seeds for the next season. The sun was bright, and the air smelled of earth and fresh grass. The Indian Premier League (IPL) is the biggest cricket league in the world. People all over the world watch the matches and cheer for their favourite teams.


Terrorism is a big danger to peace and safety. It causes harm to people and creates fear in cities and villages. When such attacks happen, they leave behind pain and sadness. To fight terrorism, we need strong laws, alert security forces, and support from people who care about peace and safety.
"""

docs = text_splitter.create_documents([sample])
print(len(docs))
print(docs)


