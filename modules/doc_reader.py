import pdfplumber
from docx import Document
import re

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

def detect_blank_fields(text):
    """
    Scans document text and returns a list of detected blank fields.
    Only detects fields representable in plain extracted text —
    see project notes for visual/layout-only field types out of scope.
    """
    patterns = [
        (r'_{3,}\s*\(([^)]+)\)', 'labeled_blank', 'high'),
        (r'\[([^\]]+)\]', 'bracket_placeholder', 'high'),
        (r'\{\{([^}]+)\}\}', 'template_placeholder', 'high'),
        (r'\b(Yes)\s*/\s*(No)\b', 'yes_no_pair', 'high'),
        (r'(Signature)\s*:?\s*_{3,}', 'signature_line', 'high'),
        (r'(Date)\s*:?\s*_{3,}', 'date_line', 'high'),
        (r'☐', 'checkbox', 'high'),
        (r'\(([^)]{1,60})\)', 'paren_placeholder', 'medium'),
        (r'_{3,}', 'bare_blank', 'medium'),  # NEW: unlabeled underscore runs
    ]

    # Labels that might appear with NO underscores at all — lower confidence
    weak_patterns = [
        (r'(Signature)\s*:\s*$', 'signature_line_weak', 'low'),
        (r'(Date)\s*:\s*$', 'date_line_weak', 'low'),
    ]

    fields = []
    covered_spans = []  # tracks which parts of the text are already claimed

    def is_overlapping(start, end):
        return any(start < c_end and end > c_start for c_start, c_end in covered_spans)

    def guess_label_from_context(start):
        preceding = text[max(0, start - 30):start]
        words = re.findall(r'[A-Za-z]+', preceding)
        return f"{words[-1]} (guessed)" if words else "Unlabeled blank"

    for pattern, field_type, confidence in patterns:
        for match in re.finditer(pattern, text):
            start, end = match.span()
            if is_overlapping(start, end):
                continue
            covered_spans.append((start, end))

            label = match.group(1).strip() if match.groups() else None
            if label and re.fullmatch(r'[_\s]*', label):
                label = None  # e.g. "( _________________)" — parens around blanks, no real label
            if not label:
                label = guess_label_from_context(start)

            fields.append({
                "full_match": match.group(0),
                "label": label,
                "type": field_type,
                "confidence": confidence,
                "position": start
            })

    for pattern, field_type, confidence in weak_patterns:
        for match in re.finditer(pattern, text, re.MULTILINE):
            start, end = match.span()
            if is_overlapping(start, end):
                continue
            covered_spans.append((start, end))
            fields.append({
                "full_match": match.group(0),
                "label": match.group(1).strip(),
                "type": field_type,
                "confidence": confidence,
                "position": start
            })

    fields.sort(key=lambda f: f["position"])
    return fields