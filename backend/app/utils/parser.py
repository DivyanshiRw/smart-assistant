# backend/app/utils/parser.py
import io
import fitz  # PyMuPDF

def parse_document(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    
    elif filename.lower().endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore").strip()
    
    else:
        return "Unsupported file type. Please upload PDF or TXT."
