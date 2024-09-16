# load_profiles.py
from pptx import Presentation
from pathlib import Path
import re
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from config import get_db_connection_string  # Use the config file for DB connection

# Set up Azure SQL connection using SQLAlchemy
DATABASE_URL = get_db_connection_string()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

# Define the consultants table
consultants_table = Table(
    'consultants', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('profile_text', String)
)

metadata.create_all(engine)

# Directory containing PowerPoint profiles
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

def load_profiles_to_database():
    files = directory.iterdir()

    for file in files:
        file_name = file.name
        consultant_name = extract_consultant_name(file_name)

        # Extract and clean text
        raw_text = extract_text_from_pptx(file)
        cleaned_text = raw_text.replace("\n", " ").replace("\t", " ").strip()  # Basic cleaning

        # Insert profile data into the database
        insert_query = consultants_table.insert().values(name=consultant_name, profile_text=cleaned_text)
        session.execute(insert_query)
    
    session.commit()

if __name__ == "__main__":
    load_profiles_to_database()
    print("Profiles have been loaded into the database.")
