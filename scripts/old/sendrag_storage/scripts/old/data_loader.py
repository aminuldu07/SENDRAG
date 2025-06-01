import os
import PyPDF2
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_string()

def extract_text_from_folder(folder_path):
    text_data = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".pdf"):
            text_data.append(extract_text_from_pdf(file_path))
        elif file.endswith(".csv"):
            text_data.append(extract_text_from_csv(file_path))
    return "\n".join(text_data)
