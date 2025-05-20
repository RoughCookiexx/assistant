import os
import action
import json
import threading
import uuid
import yaml


from action.action import BaseAction
from action.registry import ACTION_HANDLERS
from interface import aws_cognito
from interface import aws_pinpoint
from interface import aws_s3
from interface import chat
from interface import transcribe
from interface import tts
from services import intent
from util import file_tools, logger

log = logger.setup_logger()


with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
BUCKET_NAME = config['aws']['bucket_name']

with open('prompts.yaml', 'r') as prompt_file:
        prompts = yaml.safe_load(prompt_file)

def handle_command(audio_file_key, device_token, user_token):
    user_id = aws_cognito.get_user_id(user_token)
    log.info(f"Handling command from file {audio_file_key}")
    
    # Decide what action was requested
    command_text = transcribe.transcribe_audio(audio_file_key, BUCKET_NAME)
    action_name = intent.determine_intent(command_text)
    #TODO: ADD METADATA HERE! (remove user_id)
    action_json = intent.resolve_intent_parameters(action_name, command_text, user_id)
    action = ACTION_HANDLERS[action_name]
    action_model = action['model'].from_json(action_json)
    log.info(f'Chat Jippity decided we should run this action:\n{action_model}')

    # If the client handles this action, skip processing
    results = None
    if action_model.run_on_server:
        results = action['function'](action_model)

    # Push notice that the action was done
    announce_action_results(command=command_text, action_model=action_model, device_token=device_token, results=results)

def announce_action_results(command, action_model: BaseAction, device_token, results=None):
    if action_model.run_on_server:
        response = chat.message(prompts['handled_message'], f"{command}\n\n{results}")
    else:
        response = chat.message(prompts['client_handling_message'], command)

    speech = tts.speak(response)
    file_name = f'{uuid.uuid4()}.wav'
    file_tools.base64_to_file(speech.audio_base_64, f'tmp/{file_name}')
    aws_s3.upload(BUCKET_NAME, f'tmp/{file_name}', file_name)
    os.remove(f'tmp/{file_name}')

    log.info(f'Sending response to device {device_token}')
    aws_pinpoint.push(device_token, 'Url', file_name)

