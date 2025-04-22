import action
import json
import threading
import uuid
import yaml


from action.action import BaseAction
from action.registry import ACTION_HANDLERS
from interface import aws_s3
from interface import aws_pinpoint
from interface import chat
from interface import transcribe
from interface import tts
from services import intent
from util import file_tools, logger

log = logger.setup_logger()


with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 

def handle_command(audio_file_key, device_token):
    log.info(f"Handling command from file {audio_file_key}")
    
    # Decide what action was requested
    command_text = transcribe.transcribe_audio(audio_file_key, BUCKET_NAME)
    action_name = intent.determine_intent(command_text)
    action_json = intent.resolve_intent_parameters(action_name, command_text)
    action = ACTION_HANDLERS[action_name]['model'].from_json(action_json)

    # If the client handles this action, skip processing
    results = None
    if action.run_on_server:
        # results = dispatch_action(action)
        results = ACTION_HANDLERS[action_name]['function'](action)

    # Push notice that the action was done
    announce_action_results(command=command_text, action=action, device_token=device_token, results=results)

def dispatch_action(action):
    if action["run_on"] == "server":
        handler = ACTION_HANDLERS.get(action["function"])
        if not handler:
            raise ValueError(f"No handler found for action '{action["function"]}'")
    else:
        raise ValueError(f"Action '{action["name"]}' must be handled by client")
    
    args = {item['param']: item['value'] for item in action['params']}

    return handler(**args)

def announce_action_results(command, action: BaseAction, device_token, results=None):
    if action.run_on_server:
        response = chat.message(intents['handled_message'], f"{command}\n\n{results}")
    else:
        response = chat.message(intents['client_handling_message'], command)

    speech = tts.speak(response)
    file_name = f'{uuid.uuid4()}.wav'
    file_tools.base64_to_file(speech.audio_base_64, file_name)
    aws_s3.upload(BUCKET_NAME, file_name, file_name)

    log.info(f'Sending response to device {device_token}')
    aws_pinpoint.push(device_token, 'Url', file_name)

