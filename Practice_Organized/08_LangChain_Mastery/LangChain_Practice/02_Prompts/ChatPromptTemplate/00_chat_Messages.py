from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Gemini 2.5 Flash model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# messages= [
# {'role':'system','content':"You are a helpful AI Assistant"},
# {'role':'user','content':'Tell me how to use trackpad in laptop'} ]

# result = model.invoke(messages)

# messages.append({'assistant': result.content})

# print(messages)

# message list
messages = [
    SystemMessage(content='You are a helpful assistant'),
    HumanMessage(content='Tell me how to use trackpad in laptop')
]

# invoke model
result = model.invoke(messages)

# append reply to history
messages.append(AIMessage(content=result.content))

messages.append(HumanMessage(content="how the right click work on it"))

result2 = model.invoke(messages)

messages.append(AIMessage(content=result2.content))
print(messages)
