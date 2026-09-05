from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Use Gemini Flash 2.5 model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Simple JSON schema
json_schema = {
    "title": "MovieFeedback",
    "type": "object",
    "properties": {
        "movie": {"type": "string"},
        "summary": {"type": "string"},
        "sentiment": {"type": "string", "enum": ["pos", "neg", "neutral"]},
        "likes": {"type": "array", "items": {"type": "string"}},
        "dislikes": {"type": "array", "items": {"type": "string"}},
        "reviewer": {"type": "string"},
    },
    "required": ["movie", "summary", "sentiment"]
}

structured_model = model.with_structured_output(json_schema)

result = structured_model.invoke("""
I recently watched 'Interstellar'.  
The visuals were breathtaking and the music by Hans Zimmer gave me goosebumps.  
The story was emotional, especially the father-daughter arc.  

However, the long runtime felt exhausting,  
and some scientific explanations were confusing for me.

Reviewed by Rahul Dev.
""")

print(type(result))
print(result)
