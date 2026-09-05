from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")


model = ChatOpenAI(model="gpt-4o", temperature=0)
model = model.with_structured_output(Joke)

result = model.invoke("Tell me a joke about cats")
print(result)
