import re
import logging

def clean(text: str):
    # Replace all single quotes with double quotes
    return re.sub(r"'", '"', text) if "'" in text else text

def extract_json_array(text: str):
    # Extract a JSON array by taking everything from [ to ]
    logging.debug(f"Extracting JSON array from: {text}")
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def extract_markdown_code(text: str):
    # Extract code block from markdown
    match = re.search(r'```(?:\w+)?\s*\n(.*?)(?=^```)', text, re.DOTALL | re.MULTILINE)
    
    if match:
        return match.group(1).strip()
    
    # Return the original text if no code block is found
    return text
