import os
import pdfplumber

# OCR imports (safe)
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False


# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_with_pdfplumber(path):
    text = ""

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDFPlumber error: {e}")
        return ""

    return text.strip()


def extract_with_ocr(path):
    if not OCR_AVAILABLE:
        print("OCR not available, skipping scanned PDF")
        return ""

    print("Using OCR fallback...")

    text = ""

    try:
        images = convert_from_path(path)

        for i, img in enumerate(images):
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"

    except Exception as e:
        print(f"OCR failed: {e}")
        return ""

    return text.strip()


def load_pdf(path):

    # 1 Try normal extraction
    text = extract_with_pdfplumber(path)

    # 2️ If empty → OCR fallback
    if len(text) < 20:
        print("Weak text extraction → trying OCR...")
        text = extract_with_ocr(path)

    # 3️ Final fallback
    if not text or len(text.strip()) == 0:
        print(f"No usable text from: {path}")
        return ""

    return text


def load_file(path):

    if path.endswith(".txt"):
        return load_txt(path)

    if path.endswith(".pdf"):
        return load_pdf(path)

    raise ValueError("Unsupported file type")