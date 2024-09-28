import json
import logging
import subprocess
import utils.config as c
import utils.funcs as funcs

from classes.llm import LLM

def call(llm: LLM = None, logger: logging.Logger = None, additional_context: str = ""):
    config = c.load_config()
    project = config.get("project").get("path")
    sys_info = funcs.get_device_information()
    prompt = config.get("llm").get("base_prompt_for_git") \
        .replace("{{PROJECT}}", project).replace("{{INFO}}", sys_info)
    
    if additional_context != "":
        prompt = prompt.replace("{{CONTEXT}}", additional_context)
        
    logger.info(prompt)
    
    rspns = llm.ask(prompt=prompt, save=False)
    to_json: list = json.loads(funcs.extract_json_array(rspns))
    
    for command in to_json:
        command.replace("`", "")
        if "config" not in prompt and "config" in command:
            to_json.remove(command)
    
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
            except Exception as e:
                logger.error(f"Encountered error while sending command `{command}`: {e}")

        output, error = session.communicate()

        for idx, command in enumerate(to_json):
            if error:
                logger.error(f"Command failed: {command} \nError: {error}")
            else:
                logger.info(f"Command succeeded: {command}")
            command_results.append({
                "command": command,
                "output": output,
                "error": error
            })
