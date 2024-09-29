import json
import uuid
import asyncio
import logging
import edge_tts
import subprocess
import utils.config as c
import utils.funcs as funcs

from classes.llm import LLM
from playsound import playsound

async def generate_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    file_name = f"{str(uuid.uuid4())}.mp3"
    await communicate.save(file_name)
    
    return file_name

def call(llm: LLM = None, logger: logging.Logger = None, additional_context: str = ""):
    config = c.load_config()
    if not additional_context:
        logger.debug("No question present.")
        return None
    
    voice = config.get("tts").get("voice")
    
    prompt = config.get("llm").get("base_prompt_for_question") \
        .replace("{{QUESTION}}", additional_context)
        
    rspns = llm.ask(prompt, save=False)
    tts_file_name = asyncio.run(generate_audio(rspns, voice))
    
    logger.info("Speaking...")
    playsound(tts_file_name)
