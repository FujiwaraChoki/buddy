import json
import ollama
import logging
import utils.config as c

class LLM:
    def __init__(self):
        self.model = c.load_config()['llm']['model']
        self.logger = logging.getLogger(__name__)
        self.message_history = self._load_message_history()  # Ensure it's always a list
    
    def _load_message_history(self):
        self.logger.info('Loading message history...')
        message_history_path = c.load_config()['llm']['message_history_path']

        try:
            with open(message_history_path, 'r') as f:
                # Load JSON or return an empty list if file is empty or content is None
                return json.load(f) or []
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.error('Message history file not found or invalid. Creating new file...')
            return []
    
    def _add_message_to_history(self, message):
        self.message_history.append(message)
        message_history_path = c.load_config()['llm']['message_history_path']
        
        with open(message_history_path, 'w') as f:
            json.dump(self.message_history, f)
            
    def _generate_response(self, message):
        # Add system prompt to message history
        if len(self.message_history) == 0:
            self.message_history.insert(0, {
                'role': 'system',
                'content': c.load_config()['llm']['sys_prompt']
            })
        
        response = ollama.chat(model=self.model, messages=self.message_history)
        
        return response.get('message').get('content')
        
    def _ask(self, prompt: str = ''):
        self._add_message_to_history({
            'role': 'user',
            'content': prompt
        })
        response = self._generate_response(prompt)
        self._add_message_to_history({
            'role': 'system',
            'content': response
        })
        self.logger.info('Response: %s', response)
        return response
