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
    for full_name, abbr in state_abbr.items():
        text = re.sub(r'\b' + re.escape(full_name) + r'\b', abbr, text)
    return text

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing unwanted characters, fixing common OCR errors, and trimming spaces.
    """
    text = re.sub(r'[\u000b\n]+', ' ', text)  # Replace unwanted characters with space
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces and trim
    return text

def extract_fields(cleaned_text: str) -> Dict[str, Any]:
    """
    Extract relevant fields such as name, title, email, mobile, and location from cleaned text.
    """
    # Define regex patterns for extracting relevant information
    name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
    title_pattern = r'\b(Sr\. Consultant|Data Engineer|Sr\. Manager|Consultant|Manager)\b'
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    mobile_pattern = r'\(\d{3}\) \d{3}-\d{4}'
    location_pattern = r'([A-Za-z ]+),\s?([A-Z]{2})'

    # Search for matches in the cleaned text
    name_match = re.search(name_pattern, cleaned_text)
    title_match = re.search(title_pattern, cleaned_text)
    email_match = re.search(email_pattern, cleaned_text)
    mobile_match = re.search(mobile_pattern, cleaned_text)
    location_match = re.search(location_pattern, cleaned_text)

    parsed_data = {
        'name': name_match.group() if name_match else '',
        'title': title_match.group() if title_match else '',
        'email': email_match.group() if email_match else '',
        'mobile': mobile_match.group() if mobile_match else '',
        'location': f"{location_match.group(1)}, {location_match.group(2)}" if location_match else ''
    }

    return parsed_data

def parse_slide(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse data from a slide and extract relevant fields.
    """
    raw_text = slide_data.get('raw_data', '')
    cleaned_text = clean_text(raw_text)
    cleaned_text = convert_state_names_to_abbr(cleaned_text)
    extracted_fields = extract_fields(cleaned_text)

    # Extract additional text data after the title
    if extracted_fields['title']:
        title_index = cleaned_text.find(extracted_fields['title'])
        data_text = cleaned_text[title_index + len(extracted_fields['title']):].strip()
        extracted_fields['data'] = clean_text(data_text)
    else:
        extracted_fields['data'] = ''

    return extracted_fields

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
