import action
import json
import threading
import uuid
import yaml


from action.registry import ACTION_HANDLERS
from interface import aws_s3
from interface import chat
from interface import transcribe
from interface import tts
from services import intent
from util import file_tools, logger, yaml_tools

log = logger.setup_logger()


with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 

def handle_command(audio_file_key):
    # Decide what action was requested
    command_text = transcribe.transcribe_audio(audio_file_key, BUCKET_NAME)
    intent_name = intent.determine_intent(command_text)
    command_json = intent.resolve_intent_parameters(intent_name, command_text)
    command_action = json.loads(str(command_json))

    # If the client handles this action, skip processing
    results = None
    action_run_on_server = yaml_tools.match_yaml_pair(intents, 'name', intent_name) 
    if action_run_on_server:
        results = dispatch_action(command_action)

    # Push notice that the action was done
    announce_action_results(command_text, command_action, results)

def dispatch_action(action):
    if action["run_on"] == "server":
        handler = ACTION_HANDLERS.get(action["function"])
        if not handler:
            raise ValueError(f"No handler found for action '{action["function"]}'")
    else:
        raise ValueError(f"Action '{action["name"]}' must be handled by client")
    
    args = {item['param']: item['value'] for item in action['params']}

    return handler(**args)

def announce_action_results(command, action, results=None):
    if action["run_on"] == "server":
        response = chat.message(intents['handled_message'], f"{command}\n\n{results}")
    else:
        response = chat.message(intents['client_handling_message'], "command")

    speech = tts.speak(response)
    file_name = f'tmp/audio/{uuid.uuid4()}.wav'
    file_tools.base64_to_file(speech.audio_base_64, file_name)
    aws_s3.upload(BUCKET_NAME, file_name, file_name)

    # TODO: PUSH NOTIFICATION TO CLIENT
