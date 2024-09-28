import re
import json
import logging
import platform

def clean(text: str):
    return re.sub(r"'", '"', text) if "'" in text else text

def extract_json_array(text: str):
    logging.debug(f"Extracting JSON array from: {text}")
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def extract_markdown_code(text: str):
    match = re.search(r'```(?:\w+)?\s*\n(.*?)(?=^```)', text, re.DOTALL | re.MULTILINE)
    
    if match:
        return match.group(1).strip()
    return text

def get_device_information():
    device_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    return json.dumps(device_info, indent=4)

def get_shell_command():
    current_os = platform.system()
    
    if current_os == "Windows":
        return ["cmd.exe"]
    else:
        return ["/bin/bash"]
