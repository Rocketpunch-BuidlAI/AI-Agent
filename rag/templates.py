from langchain_core.prompts import PromptTemplate

extract_metadata_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
        You are an AI assistant that extracts metadata from a cover letter.
        The metadata should include the following fields:
        - id: A unique identifier for the cover letter
        - contributions: The percentage contribution of each source in the cover letter

        Here is the cover letter text:
        {text}

        Please provide the metadata in JSON format.
    """,
)


enhance_prompt = PromptTemplate(
    input_variables=["user_resume_text", "context", "custom prompt"],
    template="""
    You are a professional cover letter enhancer.

    Below is a candidate cover letter:
    ----------------------------
    {user_resume_text}

    Improve this coverletter using the following pieces of context:
    {context}
    
    Use similar phrasing, highlight relevant skills, and make it ATS-friendly.

    The cover letter format should be:
    {custom_prompt} 

    Provide a rewritten version of the cover letter, and list the sources used for the enhancements.

    Do not include the sources in the cover letter text.

    The sources should include:
    - Source ID
    - Contribution percentage
    The contribution percentages should add up to 100%.
    """,
)
