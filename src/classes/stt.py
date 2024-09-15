import logging
import speech_recognition as sr
import time

class SpeechToText:
    def __init__(self, source='mic'):
        """
        :param source: one of 'mic', 'file'
        """
        self._logger = logging.getLogger(__name__)
        self._source = source
        self._recognizer = sr.Recognizer()

    def transcribe(self, duration: int = 1):
        if duration == 0:
            while True:
                try:
                    text = self._employ_speech_to_text(duration=duration)
                    if text:
                        return text
                except Exception as e:
                    self._logger.error(f"Error during transcription: {e}")
                time.sleep(3)  # Adjust sleep time as needed
        else:
            return self._employ_speech_to_text(duration=duration)

    def _employ_speech_to_text(self, duration) -> str:
        self._logger.info('Starting Transcription...')

        try:
            with (sr.Microphone() if self._source == 'mic' else sr.AudioFile(self._source)) as src:
                self._recognizer.adjust_for_ambient_noise(src)
                audio = self._recognizer.listen(src, timeout=duration)
                text = self._recognizer.recognize_google(audio)

                if not text:
                    self._logger.info('No speech detected. Re-recording...')
                    return self._employ_speech_to_text(duration=duration)

                self._logger.info('Transcription: %s', text)
                return text
        except sr.WaitTimeoutError:
            self._logger.error('Listening timed out while waiting for phrase to start')
            return ''
        except sr.UnknownValueError:
            self._logger.error('Google Speech Recognition could not understand the audio')
            return ''
        except sr.RequestError as e:
            self._logger.error(f'Could not request results from Google Speech Recognition service; {e}')
            return ''
        except Exception as e:
            self._logger.error(f'An unexpected error occurred: {e}')
            return ''
