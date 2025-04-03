import random
import string
import threading
import yaml

from interface.aws_s3 import AwsS3
from interface import chat
from interface import elevenlabs
from interface import transcribe
from services import intent
from util import logger
from util import yaml_tools

log = logger.setup_logger()


with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']
s3 = AwsS3(BUCKET_NAME)

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 

def handle_command(audio_file_key):
    # Decide what action was requested
    command_text = transcribe_from_bucket(audio_file_key)
    command_intent = intent.determine_intent(command_text)

    # Return a message saying what action is being taken
    thread = threading.Thread(target=send_processing_message, args=[command_intent])
    thread.start()

    # Do the action
    intent.handle_intent(command_intent)

    # Push notice that the action was done

def transcribe_from_bucket(audio_file_key):
    random_filename = f"tmp/audio/{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
    s3.download(audio_file_key, f'{random_filename}.wav')

    return transcribe.transcribe_audio(f'{random_filename}.wav')

def send_processing_message(command_intent):
    response_text = chat.message( f"{intents['processing_message']}\n\n",command_intent)
    speach_response = elevenlabs.tts_request(response_text)
