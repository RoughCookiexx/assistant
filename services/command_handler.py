import random
import string
import yaml

from interface.aws_s3 import AwsS3
from interface import transcribe
from services import intent
from util import logger
from util import yaml_tools

log = logger.setup_logger()


with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']
s3 = AwsS3(BUCKET_NAME)

def handle_command(audio_file_key):
    command_text = transcribe_from_bucket(audio_file_key)
    intent = intent.determine_intent(command_text)
    intent.handle_inte

def transcribe_from_bucket(audio_file_key):
    random_filename = f"tmp/audio/{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
    s3.download(audio_file_key, f'{random_filename}.wav')

    return transcribe.transcribe_audio(f'{random_filename}.wav')


