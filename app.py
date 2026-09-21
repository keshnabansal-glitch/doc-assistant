import streamlit as st
from modules.doc_reader import extract_text, detect_blank_fields
from modules.ocr import extract_text_from_image
from modules.ai_engine import summarize_document, answer_question

st.title("Document Assistant")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(uploaded_file)
    else:
        text = extract_text(uploaded_file)

    if text:
        st.subheader("Extracted Text")
        st.text_area("Preview", text, height=300)

        if st.button("Summarize Document"):
            with st.spinner("Analyzing document..."):
                summary = summarize_document(text)
            st.subheader("Summary")
            st.write(summary)

        st.subheader("Ask a Question")
        question = st.text_input("Ask something about this document:")
        if question:
            with st.spinner("Finding your answer..."):
                answer = answer_question(text, question)
            st.write(answer)

        st.subheader("Detected Blank Fields")
        fields = detect_blank_fields(text)

        if fields:
            for i, field in enumerate(fields, start=1):
                confidence_tag = "⚠️ low confidence" if field["confidence"] == "low" else ""
                st.write(f"{i}. **{field['label']}** ({field['type']}) {confidence_tag}")
        else:
            st.info("No fillable blanks detected in this document.")
    else:
        st.error("Sorry, this file type isn't supported.")