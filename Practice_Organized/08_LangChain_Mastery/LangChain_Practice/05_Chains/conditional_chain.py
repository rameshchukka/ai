from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of the feedback')


parser2 = PydanticOutputParser(pydantic_object=Feedback)

print("parser instructions: " + parser2.get_format_instructions())

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into postive or negative \n {review} \n {parser_instruction}',
    input_variables=['review'],
    partial_variables={'parser_instruction':parser2.get_format_instructions()}
)

print("prompt1 output: " + str(prompt1.invoke({'review': 'This is a bad phone'})))

classifier_chain = prompt1 | model | parser2

prompt2 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

prompt3 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)


# RunnableBranch(
#     (condition1, runnable1),
#     (condition2, runnable2),
#     ...
#     default_runnable
# )

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt2 | model | parser),
    (lambda x:x.sentiment == 'negative', prompt3 | model | parser),
    RunnableLambda(lambda x: "could not find sentiment")
)


chain = classifier_chain | branch_chain

print(chain.invoke({'review': 'This is a bad phone'}))

chain.get_graph().print_ascii()