from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # You can also use gemini-1.5-pro etc.
    temperature=0.7
)

# Initialize empty chat history
chat_history = []

# Create chat template with history placeholder
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

print("Chat started. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    # Create prompt including history
    prompt = chat_template.invoke({
        "chat_history": chat_history,
        "query": user_input
    })

    # Call Gemini
    response = model.invoke(prompt)

    # Print response
    print("AI:", response.content)

    # Update chat history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))