import json
import ollama
import logging
import utils.config as c

class LLM:
    def __init__(self):
        config = c.load_config()
        self.model = config['llm']['model']
        self.message_history_path = config['llm']['message_history_path']
        self.sys_prompt = config['llm']['sys_prompt']

        self.logger = logging.getLogger(__name__)
        self.message_history = self._load_message_history()
        self.logger.debug(f"Initial message history loaded: {self.message_history}")

    def _load_message_history(self):
        self.logger.info('Loading message history...')

        try:
            with open(self.message_history_path, 'r') as f:
                return json.load(f) or []
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning('Message history file not found or invalid. Creating new file...')
            return []

    def _add_message_to_history(self, message):
        self.message_history.append(message)
        self.logger.debug(f"Message added to history: {message}")
        
        try:
            with open(self.message_history_path, 'w') as f:
                json.dump(self.message_history, f)
                self.logger.debug(f"Message history saved: {self.message_history}")
        except Exception as e:
            self.logger.error(f"Failed to save message history: {e}")

    def _generate_response(self):
        try:
            response = ollama.chat(model=self.model, messages=self.message_history)
            return response.get('message', {}).get('content', '')
        except Exception as e:
            self.logger.error(f"Failed to generate response: {e}")
            return ''

    def save_message_history(self):
        try:
            with open(self.message_history_path, 'w') as f:
                json.dump(self.message_history, f)
                self.logger.debug(f"Message history saved: {self.message_history}")
        except Exception as e:
            self.logger.error(f"Failed to save message history: {e}")

    def _ask(self, prompt: str = ''):
        if not self.message_history:
            self.logger.info('Message history is empty, adding System Prompt.')
            self.message_history.insert(0, {
                'role': 'system',
                'content': self.sys_prompt
            })
            self.logger.debug(f"System prompt inserted: {self.message_history[0]}")
            self.save_message_history()
        
        self._add_message_to_history({
            'role': 'user',
            'content': prompt
        })
        
        response = self._generate_response()
        
        self._add_message_to_history({
            'role': 'assistant',
            'content': response
        })
        
        self.logger.info('Response: %s', response)
        return response
