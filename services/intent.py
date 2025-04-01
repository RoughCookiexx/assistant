import random
import re
import string
import yaml

from interface.aws_s3 import AwsS3
from interface import chat
from interface import transcribe
from util import logger

log = logger.setup_logger()

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']
s3 = AwsS3(BUCKET_NAME)

def determine_intent(audio_file_key):
    random_filename = f"tmp/audio/{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
    s3.download(audio_file_key, f'{random_filename}.wav')
    text = transcribe.transcribe_audio(f'{random_filename}.wav')
    response = chat.chat(f'{intents['request_message']}\n\n{','.join(INTENT_LIST)}', text)
    log.info(response)


def handle_intent(intent_name, params):
    raise NotImplementedError("This function has not been implemented yet")

