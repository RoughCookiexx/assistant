import yaml

from interface import chat
from interface import transcribe
from util import logger
from util import yaml_tools

log = logger.setup_logger()

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 


def determine_intent(text):
    intent_response = chat.message(f'{intents['intent_message']}\n\n{','.join(INTENT_LIST)}', text)
    log.info(f'Intent: {intent_response}')

    intent_yaml_string = yaml_tools.match_yaml_pair(intents, 'name', intent_response)
    action_response = chat.message(f"{intents['action_message']}\n\n", intent_yaml_string)
    log.info(f'Action: {action_response}')

    return action_response


def handle_intent(intent_yaml):

    processing_yaml = yaml.safe_load(intent_yaml)
    if processing_yaml["run_on"] == "server":
        pass # TODO: Run the function with params from the yaml object then push a voice message to the client
    else:
        pass # TODO: Push the results back to the client

