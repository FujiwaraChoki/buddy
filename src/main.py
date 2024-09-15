import logging
import classes.stt as stt
import classes.llm as llm
import speech_recognition as sr


def main():
    LOGGER = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    
    
    STT = stt.SpeechToText()
    LLM = llm.LLM()

    if not STT:
        LOGGER.error('STT class cannot be uninstantiated. Please try again.')
        return

    while True:
        try:
            text = STT.transcribe(duration=3)
        except sr.exceptions.UnknownValueError as e:
            LOGGER.error('Could not transcribe speech: %s', e)
            continue
        LLM._ask(prompt=text)


if __name__ == '__main__':
    main()
