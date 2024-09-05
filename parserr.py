import re
from typing import List, Dict, Any

# Dictionary to map full state names to abbreviations
state_abbr = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

def convert_state_names_to_abbr(text: str) -> str:
    """
    Convert full state names in the text to their corresponding two-letter abbreviations.
    """
    # Replace full state names with their abbreviations using the state_abbr dictionary
    for full_name, abbr in state_abbr.items():
        # Using word boundaries (\b) to ensure whole word matching
        text = re.sub(r'\b' + re.escape(full_name) + r'\b', abbr, text)
    return text

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing unwanted characters, fixing common OCR errors, and trimming spaces.
    """
    text = text.replace('\u000b', ' ').replace('\n', ' ').replace('  ', ' ').strip()
    text = re.sub(r'\s+', ' ', text)  # Remove any extra spaces
    return text

def parse_slide(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse data from a slide and extract relevant fields such as name, title, email, etc.
    """
    raw_text = slide_data.get('raw_data', '')
    cleaned_text = clean_text(raw_text)
    
    # Convert full state names to abbreviations
    cleaned_text = convert_state_names_to_abbr(cleaned_text)

    # Extract fields using refined regex patterns
    name_match = re.search(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', cleaned_text)
    title_match = re.search(r'(Sr\. Consultant|Data Engineer|Sr\. Manager)', cleaned_text)
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', cleaned_text)
    mobile_match = re.search(r'\(\d{3}\) \d{3}-\d{4}', cleaned_text)
    
    # Location regex pattern for "City, ST"
    location_match = re.search(r'\n+ ([^,]+), ([A-Z]{2}) ?', cleaned_text)

    # Extract text after the title and before the next field
    title_index = cleaned_text.find(title_match.group()) if title_match else 0
    end_of_data_index = len(cleaned_text)
    
    if email_match:
        end_of_data_index = email_match.start()
    elif mobile_match:
        end_of_data_index = mobile_match.start()
    elif location_match:
        end_of_data_index = location_match.start()

    # Extract data text after title and before the next identifiable field
    data_text = cleaned_text[title_index + len(title_match.group()):end_of_data_index].strip() if title_match else ''

    parsed_data = {
        'name': name_match.group() if name_match else '',
        'title': title_match.group() if title_match else '',
        'email': email_match.group() if email_match else '',
        'mobile': mobile_match.group() if mobile_match else '',
        'location': f"{location_match.group(1)}, {location_match.group(2)}" if location_match else '',  # Correctly capture the location
        'data': clean_text(data_text)  # Clean the rest of the data
    }
    
    return parsed_data

def parse_presentation(file_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse a presentation file's data, extract parsed data from each slide.
    """
    parsed_slides = []
    for slide in file_data:
        parsed_slide = parse_slide(slide)
        parsed_slides.append({
            'slide_num': slide['slide_num'],
            'raw_data': slide['raw_data'],
            'parsed_data': parsed_slide
        })
    return parsed_slides

def parse_files(files_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse multiple presentation files.
    """
    parsed_files = []
    for file_data in files_data:
        parsed_file = {
            'filename': file_data['filename'],
            'slides': parse_presentation(file_data['slides'])
        }
        parsed_files.append(parsed_file)
    
    return parsed_files
