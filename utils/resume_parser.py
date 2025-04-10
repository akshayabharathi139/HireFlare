import re
from PyPDF2 import PdfReader

def extract_resume_data(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    name = file.name.replace(".pdf", "")
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email.group(0) if email else "N/A"
    return name, text, email
