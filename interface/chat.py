import os
import yaml

from openai import OpenAI
from util import logger

log = logger.setup_logger()

API_KEY = os.getenv("OPENAI_API_KEY")

def message(system_message, prompt):
    log.info(f'Sending message to chatGPT: {prompt}')
    openai = OpenAI(api_key=API_KEY)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": prompt}],
        max_tokens=300
    )

    log.info('ChatGippity\'s response:')
    log.info(response)

    return response.choices[0].message.content


