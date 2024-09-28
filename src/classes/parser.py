import json
import logging


class Parser:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Parser initialized.')
        
    def parse(self, text: str):
        self._logger.info('Parsing LLM\'s response...')

        to_json = json.loads(text.strip())
                
        action = to_json.get("action")
        
        return action
