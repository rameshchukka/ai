from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# Gemini 2.5 Flash model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


#before Langchain -- traditional chat method
# chat_history = [
#     {'role':'system','content':"You are a helpful AI Assistant"}
# ]
# while True:
#     user_input = input('You: ')
#     chat_history.append({'role':'user','content':user_input})
#     if user_input == 'quit':
#         break
#     result = model.invoke(chat_history)
#     chat_history.append({'role':'assistant','content':result.content})
#     print("AI: ",result.content)

# with langchain using messges module

chat_history = [
    SystemMessage(content='You are a helpful AI assistant')
]
while True:
    user_input = input('You: ')
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'quit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)

print(chat_history)