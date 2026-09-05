from langchain_openai.chat_models import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

response = model.invoke("The sky is")
print(response.content)
