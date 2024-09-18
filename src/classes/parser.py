import json
import logging

class Parser:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Parser initialized.')
        
    def parse(self, text: str):
        self._logger.info('Parsing LLM\'s response...')
        print(text)
        
        to_json = json.loads(text)
        
        print(to_json)
        
        self._logger.info('Response parsed successfully.')
        
        action = to_json.get("action")
        commands = to_json.get("commands")
        
        return action, commands
        