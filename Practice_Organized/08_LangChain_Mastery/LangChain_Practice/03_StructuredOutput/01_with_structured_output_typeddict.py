from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

result = model.invoke("From this provide name of the player and age. Context : Sachin Tendulkar is 52 years old, as of November 2025. He was born on April 24, 1973.")

print(type(result.content))
print (result.content)

class Person(TypedDict):

    name: str
    age: int
    DOB: str

structured_model = model.with_structured_output(Person)

result = structured_model.invoke("From this provide name of the player and age. Context : Sachin Tendulkar is 52 years old, as of November 2025. He was born on April 24, 1973.")

print(type(result))
print(f"My structure output using Typeddict is \n {result}" )

