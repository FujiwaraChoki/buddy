import logging
import speech_recognition as sr


class SpeechToText:
    def __init__(self, source='mic'):
        """
        :param source: one of 'mic', 'file'
        """
        self._logger = logging.getLogger(__name__)
        self._source = source
        self._recognizer = sr.Recognizer()

    def transcribe(self, duration: int = 1):
        # If duration is 0, infinitely record, and return transcribed text every 3 seconds
        if duration == 0:
            while True:
                try:
                    return self._employ_speech_to_text(duration=duration)
                except sr.RequestError as e:
                    self._logger.error('Could not transcribe using Recognizer: %s', e)
        else:
            try:
                return self._employ_speech_to_text(duration=duration)
            except sr.RequestError as e:
                self._logger.error('Could not transcribe using Recognizer: %s', e)

    def _employ_speech_to_text(self, duration) -> str:
        self._logger.info('Starting Transcription...')

        with (sr.Microphone() if self._source == 'mic' else sr.AudioFile) as src:
            self._recognizer.adjust_for_ambient_noise(src)
            audio = self._recognizer.listen(src, timeout=duration)
            text = self._recognizer.recognize_google(audio)
            
            if not text:
                self._logger.info('No speech detected. Re-recording...')
                return self._employ_speech_to_text(duration=duration)
            
            self._logger.info('Transcription: %s', text)
            
            return text
