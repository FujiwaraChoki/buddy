import os
import json
import utils.config as c
import classes.llm as LLM

def list_all_files(dir=""):
    # Lists all files in a directory, recursively, except the ones mentioned in the c['ignore-files'] array
    file_list = []
    ignore_files = c.load_config().get("ignore-files", [])
    
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            for ignored in ignore_files:
                if ignored.get("name") is not None:
                    if ignored.get("name") in file_path:
                        file_list.append(file_path)
                elif ignored.get("extension") is not None:
                    if not file_path.endswith(ignored.get("extension")):
                        file_list.append(file_path)
                else:
                    continue
                
    return file_list

def call(llm: LLM=None, logger=None):
    logger.info("Calling Refactor.")
    
    config = c.load_config()

    # Read the code user is having trouble with (from project)
    project = config.get("project").get("path")
    
    # Comma separated files (from func above)
    cs_files = ", ".join(list_all_files(project))
    print(cs_files)
    
    altered_prompt = config.get('llm').get('base_prompt_project_recognition') \
        .replace("{{PROJECT_NAME}}", project) \
        .replace("{{FILES}}", cs_files)
    
    # Recognize what kind of project it is
    response = llm.ask(prompt=altered_prompt, save=False)
    
    to_json = json.loads(response)
    
    logger.debug(to_json)
    