import streamlit as st

from rag.rag import generate_cover_letter

info = st.text_area("Your Info")

prompt = st.text_area(
    "Prompt",
    placeholder="Paste your prompt",
    height=300,
)

if st.button("Create"):
    st.write("Create your cover letter...")

    result = generate_cover_letter(
        text=info,
        metadata=metadata,
        prompt=prompt,
    )

    st.write("Cover letter will be displayed here.")
    st.write(result)
