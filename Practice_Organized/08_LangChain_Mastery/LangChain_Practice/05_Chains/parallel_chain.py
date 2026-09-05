from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel


load_dotenv()

model1 = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

# model2: Replace Claude with HuggingFaceEndpoint model
# Example: "mistralai/Mixtral-8x7B-Instruct" or any HF Inference API model
# llm = HuggingFaceEndpoint(
#     repo_id="Nanbeige/Nanbeige4.1-3B",
#     task="text-generation"
# )
# model2 = ChatHuggingFace(llm=llm)

prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text:\n{text}',
)

prompt2 = PromptTemplate(
    template='Generate 5 short question & answer pairs from the following text:\n{text}',
    input_variables=['text'])

prompt3 = PromptTemplate(
    template='Mrge the provided notes and quiz into a single document.\nNotes:\n{notes}\n\nQuiz:\n{quiz}',
    input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model1 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = """
Support vector machines (SVMs) are a set of supervised learning methods...
"""

result = chain.invoke({'text': text})
print(result)

# visualize DAG
chain.get_graph().print_ascii()
