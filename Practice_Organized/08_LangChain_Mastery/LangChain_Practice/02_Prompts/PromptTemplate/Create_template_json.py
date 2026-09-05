from langchain_core.prompts import PromptTemplate

# template
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

template.save('template.json')
