from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import Literal

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of the feedback')


parser2 = PydanticOutputParser(pydantic_object=Feedback)

print("parser instructions: " + parser2.get_format_instructions())