import logging
import classes.stt as stt
import classes.llm as llm
import classes.parser as parser
import actions.refactor as refactor

def main():
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    STT = stt.SpeechToText()
    LLM = llm.LLM()
    PARSER = parser.Parser()

    if not STT:
        LOGGER.error('STT class cannot be uninstantiated. Please try again.')
        return

    while True:
        try:
            text = STT.transcribe(duration=3)
        except Exception as e:
            LOGGER.error('Could not transcribe speech: %s', e)
            continue
        response = LLM.ask(prompt=text, save=True)

        if not response:
            LOGGER.error('No response generated. Please try again.')
            continue

        LOGGER.info('Response: %s', response)
        parsed_response = PARSER.parse(response)

        if not parsed_response:
            LOGGER.error('Failed to parse response. Please try again.')
            continue

        action, commands = parsed_response
        LOGGER.info('Action: %s', action)
        LOGGER.info('Commands: %s', commands)
        
        action = 'refactor'

        if action == 'refactor':
            refactor.call(llm=LLM, logger=LOGGER)
        elif action == 'exit':
            LOGGER.info('Exiting...')
            break

if __name__ == '__main__':
    main()
