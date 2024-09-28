import os
import json
import logging
import subprocess
import utils.config as c
import classes.llm as LLM
import utils.funcs as funcs

def list_all_files(directory=""):
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
        .replace("{{INFO}}", funcs.get_device_information())
        
    logger.debug(f"Using the following prompt to install dependencies: {prompt}")
    
    rspns = llm.ask(prompt=prompt, save=False)
    to_json = json.loads(funcs.extract_json_array(rspns))
    
    command_results = []
    
    shell_command = funcs.get_shell_command()
    
    with subprocess.Popen(shell_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as session:
        if shell_command == ["cmd.exe"]:
            session.stdin.write(f"cd /d {project_path}\n")
        else:
            session.stdin.write(f"cd {project_path}\n")
        
        if type(to_json) == list:
            for command in to_json:
                try:
                    logger.debug(f"Executing command: {command}")
                    
                    session.stdin.write(f"{command}\n")
                    session.stdin.flush()
                    
                    output, error = session.communicate()
                    
                    command_results.append({
                        "command": command,
                        "output": output,
                        "error": error
                    })
                    
                    if error:
                        logger.error(f"Command failed: {command} \nError: {error}")
                    else:
                        logger.info(f"Command succeeded: {command}")
                        
                except Exception as error:
                    logger.error(f"Failed to execute command: {command}. Error: {error}")
        else:
            try:
                logger.debug(f"Executing command: {to_json}")
                
                session.stdin.write(f"{to_json}\n")
                session.stdin.flush()
                
                output, error = session.communicate()
                
                command_results.append({
                    "command": to_json,
                    "output": output,
                    "error": error
                })
                
                if error:
                    logger.error(f"Command failed: {to_json} \nError: {error}")
                else:
                    logger.info(f"Command succeeded: {to_json}")
                    
            except Exception as error:
                logger.error(f"Failed to execute command: {to_json}. Error: {error}")

    logger.debug(f"All commands executed. Results: {command_results}")
    
    return command_results
