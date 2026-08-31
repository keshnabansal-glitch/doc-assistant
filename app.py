import streamlit as st
from modules.doc_reader import extract_text
from modules.ocr import extract_text_from_image

st.title("Document Assistant")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(uploaded_file)
        print(text)
    else:
        text = extract_text(uploaded_file)

    if text:
        st.subheader("Extracted Text")
        st.text_area("Preview", text, height=400)
    else:
        st.error("Sorry, this file type isn't supported.")