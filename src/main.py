import logging
import asyncio

import classes.stt as stt
import classes.llm as llm
import classes.parser as parser

import actions.git as git
import actions.run as run
import actions.joke as joke
import actions.install as install
import actions.refactor as refactor
import actions.question as question

import utils.config as c
import utils.funcs as funcs

from playsound import playsound

def main():
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    STT = stt.SpeechToText()
    LLM = llm.LLM()
    PARSER = parser.Parser()
    
    voice = c.load_config().get("tts").get("voice")
    audio_file_name = asyncio.run(funcs.generate_audio("How can I help you today?", voice))
    
    playsound(audio_file_name)
    
    if not STT:
        LOGGER.error('STT class cannot be uninstantiated. Please try again.')
        return
    
    BY_SPEECH = c.load_config().get("app").get("input_method") == "speech"

    while True:
        if BY_SPEECH:
            try:
                text = STT.transcribe(duration=3)
            except Exception as e:
                LOGGER.error('Could not transcribe speech: %s', e)
                continue
        else:
            text = input("What would you like to do? ")
        response = LLM.ask(prompt=text, save=True)

        if not response:
            LOGGER.error('No response generated. Please try again.')
            continue

        LOGGER.info('Response: %s', response)
        parsed_response = PARSER.parse(response)

        if not parsed_response:
            LOGGER.error('Failed to parse response. Please try again.')
            continue

        action, context = parsed_response

        if action == 'refactor':
            refactor.call(llm=LLM, logger=LOGGER, additional_context=context)
        elif action == 'install':
            install.call(llm=LLM, logger=LOGGER)
        elif action == 'git':
            git.call(llm=LLM, logger=LOGGER, additional_context=context)
        elif action == 'question':
            question.call(llm=LLM, logger=LOGGER, additional_context=context)
        elif action == 'run':
            run.call(llm=LLM, logger=LOGGER)
        elif action == 'joke':
            joke.call(llm=LLM, logger=LOGGER, additional_context=context)
        elif action == 'exit':
            LOGGER.info('Exiting...')
            break

if __name__ == '__main__':
    main()
