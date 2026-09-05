from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# schema
class Review(TypedDict):
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[Literal["positive", "neg"], "Return sentiment of the review either negative, positive or neutral"]
    strenth: Annotated[Optional[list[str]], "Write down all the strenth inside a list"]
    weakness: Annotated[Optional[list[str]], "Write down all the Weakness inside a list"]
    name: Annotated[Optional[str], "Write the name of the reviewer"]

structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""
I watched the movie *Eternal Horizons* last night, and it left me thinking about life in an entirely new way.
The storytelling is slow but purposeful, allowing each character arc to breathe.
The visuals are breathtaking—wide shots of desolate landscapes mixed with intimate emotional moments.

The soundtrack is haunting and perfectly complements the movie’s tone.
The performances, especially by the lead actress, feel raw and authentic.
However, the movie is definitely not for everyone—the pacing is extremely slow, and some scenes drag longer than necessary.
The ending is also deliberately ambiguous, which might frustrate viewers who prefer clear resolutions.

Review by Arjun Rao
""")

print(type(result))
print(result)
