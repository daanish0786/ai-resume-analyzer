
import pdfplumber, re, io

def read_pdf(file_like_or_path):
    """Accepts an uploaded file (BytesIO) from Streamlit or a file path."""
    text = []
    if hasattr(file_like_or_path, "read"):
        # Streamlit UploadedFile
        file_like_or_path.seek(0)
        with pdfplumber.open(file_like_or_path) as pdf:
            for p in pdf.pages:
                text.append(p.extract_text() or "")
    else:
        with pdfplumber.open(file_like_or_path) as pdf:
            for p in pdf.pages:
                text.append(p.extract_text() or "")
    return "\n".join(text)

def clean_text(t: str) -> str:
    t = t or ""
    t = re.sub(r"\s+", " ", t).strip()
    return t
