import asyncio
import logging
import utils.config as c
import utils.funcs as funcs

from classes.llm import LLM
from playsound import playsound

def call(llm: LLM = None, logger: logging.Logger = None, additional_context: str = ""):
    config = c.load_config()
    voice = config.get("tts").get("voice")
    prompt = config.get("llm").get("base_prompt_for_joke")
    
    if additional_context:
        prompt += f"Here is some additional context: {additional_context}"
    
    rspns = llm.ask(prompt=prompt, save=False)
    
    tts_file_name = asyncio.run(funcs.generate_audio(rspns, voice))
    
    logger.info("Speaking...")
    playsound(tts_file_name)
