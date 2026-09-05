from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables (this will look for GOOGLE_API_KEY or GEMINI_API_KEY)
load_dotenv()

# Initialize the model using a Gemini model
# 'gemini-2.5-flash' is a fast and capable model for general tasks.
# You can also use 'gemini-2.5-pro' for higher quality results.
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=1.5)

# Invoke the model
result = model.invoke("Generate 3 creative taglines for new car brand to the market")

# Print the result
print(result.content)