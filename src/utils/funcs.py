import re
import os
import uuid
import json
import logging
import edge_tts
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

def list_all_files(c, directory=""):
    # Lists all files in a directory, recursively, except the ones mentioned in the c['ignore-files'] array
    file_list = []
    ignore_files = c.load_config().get("ignore-files", [])

    def should_ignore(file_path):
        for ignored in ignore_files:
            if "extension" in ignored and file_path.endswith(ignored["extension"]):
                return True
            if "name" in ignored and ignored["name"] in file_path:
                return True
        return False

    def add_file(path):
        if path not in file_list:
            file_list.append(path)

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path):
                add_file(file_path)

    return file_list

async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    file_name = f"{str(uuid.uuid4())}.mp3"
    await communicate.save(file_name)
    
    return file_name