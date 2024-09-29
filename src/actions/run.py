import os
import json
import platform
import subprocess
import utils.config as c
import utils.funcs as funcs

def call(llm=None, logger=None):
    config = c.load_config()
    project = config.get("project").get("path")
    
    cs_files = ", ".join(funcs.list_all_files(c, project))
    
    altered_prompt = config.get('llm').get('base_prompt_project_recognition') \
        .replace("{{PROJECT_NAME}}", project) \
        .replace("{{FILES}}", cs_files)
        
    # Recognize what kind of project it is
    response = llm.ask(prompt=altered_prompt, save=False)
    logger.debug(response)
    to_json = json.loads(funcs.clean(response))
    language = to_json.get("language")
    main_file = to_json.get("main_file")
    
    if not language:
        logger.error("Language cannot be empty.")
    
    if not main_file:
        logger.error("Main file cannot be non-existant.")
        
    main_file_contents = open(os.path.join(project, main_file), "r").read().strip()
    
    prompt = config.get("llm").get("base_prompt_for_running") \
        .replace("{{PROJECT}}", project) \
        .replace("{{FILES}}", cs_files) \
        .replace("{{LANGUAGE}}", language) \
        .replace("{{MAIN_FILE}}", main_file) \
        .replace("{{MAIN_FILE_CONTENTS}}", main_file_contents) \
        .replace("{{INFO}}", funcs.get_device_information())
        
    rspns = llm.ask(prompt=prompt, save=False)
    
    try:
        to_json = json.loads(rspns)
    except json.JSONDecodeError:
        logger.debug("Using regex to extract array")
        to_json = json.loads(funcs.extract_json_array(rspns))
        
    command_results = []
    
    shell_command = funcs.get_shell_command()
    
    with subprocess.Popen(shell_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as session:
        if shell_command == ["cmd.exe"]:
            session.stdin.write(f"cd /d {project}\n")
        else:
            session.stdin.write(f"cd {project}\n")
        
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
                
        logger.debug(f"All commands executed. Results: {command_results}")
        
        return command_results
