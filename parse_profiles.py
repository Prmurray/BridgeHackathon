from pptx import Presentation
from pathlib import Path
import re

directory = Path('./profiles/')

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing unwanted characters, fixing common OCR errors, and trimming spaces.
    """
    text = re.sub(r'[\u000b\n]+', ' ', text)  # Replace unwanted characters with space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces and trim
    return text

# Function to extract consultant name from file name
def extract_consultant_name(file_name):
    match = re.match(r"(\w+)\s+(\w+)\s+-\s+Consultant Profile", file_name)
    if match:
        first_name, last_name = match.groups()
        return f"{first_name} {last_name}"
    return "Unknown"

# Function to extract text from PowerPoint presentation
def extract_text_from_pptx(pptx_path):
    presentation = Presentation(pptx_path)
    text_runs = []
    
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                cleaned = clean_text(shape.text.strip())
                text_runs.append(cleaned)
    
    return "\n".join(text_runs)

def get_profiles():
    consultant_profiles = ""
    files = directory.iterdir()

    for file in files:
        file_name = file.name
        consultant_name = extract_consultant_name(file_name)

        # Extract and clean text
        raw_text = extract_text_from_pptx(file)
        cleaned_text = raw_text.replace("\n", " ").replace("\t", " ").strip()  # Basic cleaning

        # Store profile data
        
        consultant_profiles += f"name: {consultant_name}\n profile_text: {cleaned_text}\n\n"

    return consultant_profiles
