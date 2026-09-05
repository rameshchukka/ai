from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import load_prompt

load_dotenv()

# Initialize Gemini 2.5 Flash model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.header('Project Proposal Summarizer')

# User selections
project_title = st.text_input("Enter Project Title", "AI-Powered Chatbot System")

writing_style = st.selectbox(
    "Select Writing Style",
    ["Formal", "Beginner-Friendly", "Technical", "Business-Oriented"]
)

length = st.selectbox(
    "Select Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)

# Load prompt template
#template = load_prompt('template.json')



template = PromptTemplate(
    template="""
Generate a detailed project proposal summary for the project titled "{project_title}".
Follow these instructions:

Writing Style: {writing_style}
Length Requirement: {length}

1. Technical Details:
   - Describe the core architecture and technologies involved.
   - Provide a simple Python code snippet that illustrates the main logic.

2. Business Value:
   - Explain the expected ROI in simple terms.

3. Risks:
   - Mention key technical or business risks only if they are explicitly stated.

If information is missing, respond with: "Insufficient information available".

Ensure the proposal is clear, structured, and aligned with the writing style and length.
""",
    input_variables=['project_title', 'writing_style', 'length'],
    validate_template=True
)

prompt= template.invoke({
        'project_title': project_title,
        'writing_style': writing_style,
        'length': length
    })


# Summarize button
if st.button('Generate Proposal Summary'):
    # Combine prompt with model
    #chain = template | model
    # result = chain.invoke({
    #     'project_title': project_title,
    #     'writing_style': writing_style,
    #     'length': length
    # })
    result = model.invoke(prompt)
    st.write(result.content)
