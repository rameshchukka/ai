from langsmith import Client

client = Client()

# Create a dataset
examples = [
    ("Which country's customers spent the most? And how much did they spend?",
     "The country whose customers spent the most is the USA, with a total expenditure of $523.06"),
    ("What was the most purchased track of 2013?",
     "The most purchased track of 2013 was Hot Girl."),
    ("How many albums does the artist Led Zeppelin have?",
     "Led Zeppelin has 14 albums"),
    ("What is the total price for the album “Big Ones”?",
     "The total price for the album 'Big Ones' is 14.85"),
    ("Which sales agent made the most in sales in 2009?",
     "Steve Johnson made the most sales in 2009"),
]

dataset_name = "sql-agent-response"
if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(dataset_name=dataset_name)
    inputs, outputs = zip(
        *[({"input": text}, {"output": label}) for text, label in examples]
    )
    client.create_examples(
        inputs=inputs, outputs=outputs, dataset_id=dataset.id)
