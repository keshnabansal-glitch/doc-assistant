import streamlit as st
from modules.doc_reader import extract_text

st.title("Document Assistant")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx"])

if uploaded_file is not None:
    text = extract_text(uploaded_file)

    if text:
        st.subheader("Extracted Text")
        st.text_area("Preview", text, height=400)
    else:
        st.error("Sorry, this file type isn't supported.")