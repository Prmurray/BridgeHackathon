import os
import json
from pptx import Presentation
from parserr import extract_text_from_slide, extract_fields_from_text, clean_extracted_text


def parse_pptx_file(filepath):
    """
    Parses a .pptx file and extracts text from each slide.

    Parameters:
    - filepath: Path to the .pptx file.

    Returns:
    - A list of strings, each representing the text extracted from a slide.
    """
    prs = Presentation(filepath)
    slides_text = []

    for slide in prs.slides:
        slide_text = extract_text_from_slide(slide)
        slides_text.append(slide_text)

    return slides_text


def parse_ppt_files(directory):
    """
    Parses all .pptx files in the specified directory and extracts relevant data.

    Parameters:
    - directory: Directory path containing .pptx files.

    Returns:
    - A list of parsed data dictionaries.
    """
    parsed_files_data = []

    for filename in os.listdir(directory):
        if filename.endswith(".pptx"):
            pptx_path = os.path.join(directory, filename)
            slides_data = parse_pptx_file(pptx_path)  # Get raw text for each slide
            
            parsed_file_data = {
                "filename": filename,
                "slides": []
            }

            for slide_num, slide_text in enumerate(slides_data, start=1):
                parsed_slide_data = extract_fields_from_text(slide_text)
                cleaned_slide_data = clean_extracted_text(parsed_slide_data)
                parsed_file_data["slides"].append({
                    "slide_num": slide_num,
                    "raw_data": slide_text,
                    "parsed_data": cleaned_slide_data
                })

            parsed_files_data.append(parsed_file_data)

    return parsed_files_data


def save_parsed_data_to_json(parsed_data, output_file='parsed_data.json'):
    """
    Saves the parsed data to a JSON file.

    Parameters:
    - parsed_data: The data to save.
    - output_file: The file path to save the JSON data.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)


def main():
    """
    Main function to execute parsing and saving to JSON.
    """
    directory = 'your_directory_path_here'  # Update this to your directory path
    parsed_data = parse_ppt_files(directory)
    save_parsed_data_to_json(parsed_data)
    print(f"Parsed data saved to parsed_data.json")


if __name__ == "__main__":
    main()
