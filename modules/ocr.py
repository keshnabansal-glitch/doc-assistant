from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(uploaded_file):
    """
    Takes a Streamlit-uploaded image file, runs OCR on it, and returns the text.
    """
    image = Image.open(uploaded_file)
    return pytesseract.image_to_string(image)
