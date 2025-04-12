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
    input_variables=["user_resume_selfIntroduction", "user_resume_motivation", "user_resume_relevantExperience", "user_resume_futureAspirations", "context", "custom prompt", "user_metadata"],
    template="""
    You are a professional cover letter enhancer.

    Below is a candidate cover letter:
    ----------------------------
    Self Introduction:
    {user_resume_selfIntroduction}
    Motivation:
    {user_resume_motivation}
    Relevant Experience:
    {user_resume_relevantExperience}
    Future Aspirations:
    {user_resume_futureAspirations}
    
    Here is the metadata for the cover letter:
    ----------------------------
    {user_metadata}

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
