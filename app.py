import streamlit as st

st.title("Cover Letter Enhancer")
st.write("Upload your cover letter and get an enhanced version with suggestions for improvement.")

st.file_uploader(
    "Upload your Cover Letter",
    type=["txt", "pdf"],
)

st.text_area(
    "Extract Prompt",
    placeholder="Paste your prompt",
    height=300,
)

if st.button("Enhance"):
    st.write("Enhancing your cover letter...")
    # Call the enhance function here with the uploaded file and prompt
    # enhanced_cover_letter = enhance(original_cover_letter, prompt)
    # st.text_area("Enhanced Cover Letter", value=enhanced_cover_letter, height=300)
    st.write("Enhanced cover letter will be displayed here.")
