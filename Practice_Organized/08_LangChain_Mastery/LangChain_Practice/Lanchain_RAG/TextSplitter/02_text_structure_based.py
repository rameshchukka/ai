
#pip install -qU langchain-text-splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter,CharacterTextSplitter

text = """
Space exploration has led to incredible scientific discoveries. 
From landing on the Moon to exploring Mars, humanity continues to push the boundaries of what’s possible beyond our planet.

These missions have not only expanded our knowledge of the universe but have also contributed to advancements in technology here on Earth. 
Satellite communications, GPS, and even certain medical imaging techniques trace their roots back to innovations driven by space programs.
"""

# Initialize the splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0,
)

# Perform the split
chunks = splitter.split_text(text)

print("Recursive Splitter Output:")
print(len(chunks))
print(chunks)

char_splitter = CharacterTextSplitter(
chunk_size=100,
chunk_overlap=0,
)

chunks = splitter.split_text(text)

print("Character Splitter Output:")
print(len(chunks))
print(chunks)