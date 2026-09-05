from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#Dynamic template_text
Dynmic_template_text="""
        Use the following context to answer the question:

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

# Prompt template
template = PromptTemplate(
    template=Dynmic_template_text,
    input_variables = ['context','question'],
    validatation=True)

print(template.input_variables)

prompt= template.invoke({'context':"policy says an employee can take 5 days leave a an year", 'question':"How many days of leave can an employee take per year?"})

print(prompt)

result = model.invoke(prompt)

print(result.content)



