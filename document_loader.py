import pandas as pd
from pypdf import PdfReader
from docx import Document



def load_text_file(file):

    with open(file.name, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(file):

    reader = PdfReader(file.name)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def load_docx_file(file):

    doc = Document(file.name)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text
    
def load_excel_file(file):

    df = pd.read_excel(file.name)

    return df.to_string(index=False)
    
def load_csv_file(file):

    df = pd.read_csv(file.name)

    return df.to_string(index=False)