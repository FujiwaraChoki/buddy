import re
import json
import logging


class Parser:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info('Parser initialized.')
        
    def parse(self, text: str):
        self._logger.info('Parsing LLM\'s response...')

        try:
            # Try normal JSON parsing
            to_json = json.loads(text.strip())
        except json.JSONDecodeError:
            self._logger.warning('Normal parsing failed, attempting regex extraction...')
            # Use regex to extract the JSON object
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    to_json = json.loads(json_match.group())
                except json.JSONDecodeError:
                    self._logger.error('Failed to parse JSON object with regex.')
                    return None, None
            else:
                self._logger.error('No JSON object found using regex.')
                return None, None
                
        action = to_json.get("action")
        context = to_json.get("context")
        
        return action, context
