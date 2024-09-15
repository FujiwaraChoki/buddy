import json
import logging

class Parser:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Parser initialized.')
        
    def parse(self, text: str):
        self._logger.info('Parsing LLM\'s response...')
        
        to_json = json.loads(text)
        
        action = to_json.get('action')
        commands = to_json.get('commands')
        
        if not action:
            self._logger.error('No action found in response.')
            return
        
        if not commands:
            self._logger.error('No commands found in response.')
            return
        
        self._logger.info('Response parsed successfully.')
        
        return action, commands
        