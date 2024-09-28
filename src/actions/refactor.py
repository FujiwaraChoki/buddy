import os
import json
import logging
import utils.config as c
import classes.llm as LLM
import utils.funcs as funcs


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
            if not should_ignore(file_path):  # Skip files that match the ignore list
                add_file(file_path)

    return file_list


def call(llm: LLM = None, logger: logging.Logger = None):
    logger.info("Calling Refactor.")

    config = c.load_config()

    # Read the code user is having trouble with (from project)
    project = config.get("project").get("path")

    # Comma separated files (from func above)
    cs_files = ", ".join(list_all_files(project))

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
    
    altered_prompt_asking_about_main_file = config.get("llm").get("base_prompt_read_main_file") \
        .replace("{{FILE_NAME}}", main_file) \
        .replace("{{LANGUAGE}}", language) \
        .replace("{{FILES}}", cs_files) \
        .replace("{{CODE}}", main_file_contents)
    
    files_in_json_response = llm.ask(prompt=altered_prompt_asking_about_main_file, save=False)
    files_in_json_response = json.loads(funcs.extract_json_array(funcs.clean(files_in_json_response)))
    
    for file in files_in_json_response:
        logger.debug(f"===== REFACTORING FILE {file} START =====")
        file_contents = open(os.path.join(project, file), "r").read().strip()
        altered_prompt_for_refactor = config.get("llm").get("base_prompt_refactor_code") \
            .replace("{{PROJECT}}", project) \
            .replace("{{LANGUAGE}}", file.split(".")[-1]) \
            .replace("{{CODE}}", file_contents)
        rspns = llm.ask(prompt=altered_prompt_for_refactor, save=False)
        if not file.endswith(".md") \
            or not file.endswith(".mdx"):
            rspns = funcs.extract_markdown_code(rspns)
        logger.info(rspns)
        
        choice = input("Replace file (y/N): ")
        
        if choice.lower() == "y":
            logger.info(f"Replacing contents for file {file}")
            with open(os.path.join(project, file), "w") as f:
                f.write(rspns)
        else:
            logger.info(f"Skipping {file}")
            continue
        
        logger.debug(f"===== REFACTORING FILE {file} FINISH =====")

    return files_in_json_response if files_in_json_response else None
