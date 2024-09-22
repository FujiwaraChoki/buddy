import os
import json
import logging
import src.utils.config as c
import src.classes.llm as LLM


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
        if path not in file_list:  # Only check if it's already in the list
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
    to_json = json.loads(response)

    return to_json if to_json else None
