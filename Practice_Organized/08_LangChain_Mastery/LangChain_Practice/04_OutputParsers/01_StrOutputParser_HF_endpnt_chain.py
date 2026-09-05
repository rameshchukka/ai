from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

# if env file has some issue you can use this login from huggingface_hub
#from huggingface_hub import login
#login(token="hf_GbjRSrRLjypGu")
load_dotenv()

# while creating the huggingface token you must check Make calls to Inference Providers for HuggingFaceEndpoint to work

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

#model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

# llm = HuggingFacePipeline.from_model_id(
#     model_id="google/gemma-2-2b-it",
#     task="text-generation",
#     pipeline_kwargs={"max_new_tokens": 512, "temperature": 0.7}
# )

# Wrap it for chat format (supports messages with roles)
chat_model = ChatHuggingFace(llm=llm)

# Create prompts
template1 = PromptTemplate.from_template('Write a detailed report on {topic}')


# prompt = template1.invoke({'topic': 'black hole'})
# result = chat_model.invoke(prompt)
# print(result.content)
# strparse = StrOutputParser()
# finalresult = strparse.invoke(result.content)
# print(finalresult)

# Create chains
chain1 = template1 | chat_model

# Execute # print the output without the StrOutputParser
report = chain1.invoke({'topic': 'black hole'})
print("DETAILED REPORT:\n", report)

# with StrOutputParser so the output is properly formatted
stroutpars = StrOutputParser()

chain1 = template1 | chat_model | stroutpars
report = chain1.invoke({'topic': 'black hole'})
print("DETAILED REPORT:\n", report)