import pdfplumber
from docx import Document

def extract_text(uploaded_file):
    """
    Takes a Streamlit-uploaded file object and returns its text content as a string.
    Handles both PDF and DOCX files.
    """
    filename = uploaded_file.name

    if filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif filename.endswith(".docx"):
        doc = Document(uploaded_file)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text

    else:
        return None