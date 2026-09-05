from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# schema; here we use Field rather annotations used in TypeDict
class PlaceInsights(BaseModel):
    highlights: list[str] = Field(description="Important highlights about the place")
    summary: str = Field(description="Short summary of the place")
    ideal_for: list[str] = Field(description="Types of travelers who would enjoy this place")
    rating: Optional[int] = Field(gt=1,lt=5, description="Overall rating out of 5 if available")
    drawbacks: Optional[list[str]] = Field(default=None, description="List any drawbacks or issues")
    location: Optional[str] = Field(default=None, description="Mention the location name if present")

structured_model = model.with_structured_output(PlaceInsights)

result = structured_model.invoke("""
I recently visited Manali, a beautiful hill town in Himachal Pradesh.
The snow-capped mountains, pine forests, and rivers make it picture-perfect.
Solang Valley was the highlight — I tried paragliding for the first time and it was unforgettable.
Old Manali cafés are peaceful and great for remote work.
The only downside is the heavy traffic during peak season, and prices have gone up a lot recently.
""")

print(type(result))
print(result)
