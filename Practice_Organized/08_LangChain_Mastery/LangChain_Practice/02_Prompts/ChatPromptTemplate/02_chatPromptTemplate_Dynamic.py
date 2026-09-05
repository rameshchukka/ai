from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

## the below supposed to work in langchain but unfortunately doesnot work for dynamic prompt

# chat_template = ChatPromptTemplate([
#     (SystemMessage ('You are a helpful {domain} expert')),
#     (HumanMessage(content= 'Explain in simple terms, what is {topic}'))
#     ])

# prompt = chat_template.invoke({
#     'domain': 'astronomy',
#     'topic': 'black holes'
# })

# print(prompt)

## This is the structure will work for dynamic prompt

chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful {domain} expert'),
    ('human', 'Explain in simple terms, what is {topic}')
])

prompt = chat_template.invoke({
    'domain': 'astronomy',
    'topic': 'black holes'
})

print(prompt)

# This preserves:

    # Role separation
    # System instructions
    # Multi-turn logic
    # Memory integration

# This matters a LOT in:

    # Agents
    # RAG
    # Tool calling
    # Conversational systems