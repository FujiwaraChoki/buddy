import os
import json
import logging
import platform
import subprocess
import utils.config as c
import classes.llm as LLM
import utils.funcs as funcs

def get_device_information():
    # Returns basic device information
    device_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }
    return json.dumps(device_info, indent=4)


def list_all_files(directory=""):
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

def call(llm: LLM = None, logger: logging.Logger = None):
    logger.debug("Calling Install.")
    
    config = c.load_config()
    project_path = config.get("project").get("path")
    
    cs_files = ", ".join(list_all_files(project_path))
    
    prompt = config.get("llm").get("base_prompt_for_installation") \
        .replace("{{PROJECT}}", project_path) \
        .replace("{{FILES}}", cs_files) \
        .replace("{{INFO}}", get_device_information())
        
    logger.debug(f"Using following prompt to install dependencies: {prompt}")
    
    rspns = llm.ask(prompt=prompt, save=False)
    to_json = json.loads(funcs.extract_json_array(rspns))
    
    command_results = []
    
    if type(to_json) == list:
        for command in to_json:
            try:
                logger.debug(f"Executing command: {command}")
                
                result = os.system(command)
                
                command_results.append({
                    "command": command,
                    "return_code": result
                })
                
                if result != 0:
                    logger.error(f"Command failed: {command} \nError: {result.stderr}")
                else:
                    logger.info(f"Command succeeded: {command}")
                    
            except Exception as error:
                logger.error(f"Failed to execute command: {command}. Error: {error}")
    else:
        logger.debug(f"Executing command: {to_json}")
        result = os.system(to_json)
        
        command_results.append({
            "command": to_json,
            "return_code": result
        })
        
        if result != 0:
            logger.error(f"Command failed: {to_json} \nError: {result.stderr}")
        else:
            logger.info(f"Command succeeded: {to_json}")

    # Log final result of all commands
    logger.debug(f"All commands executed. Results: {command_results}")
    
    return command_results