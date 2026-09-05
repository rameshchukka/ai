from langchain_openai.chat_models import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

completion = model.invoke("Hi there!")
# Hi!

completions = model.batch(["Hi there!", "Bye!"])
# ['Hi!', 'See you!']

for token in model.stream("Bye!"):
    print(token)
    # Good
    # bye
    # !
