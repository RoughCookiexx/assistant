import yaml

from interface import chat
from util import logger
from util import yaml_tools

log = logger.setup_logger()

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)
INTENT_LIST = ', '.join(intent["name"] for intent in intents["intents"]) 


def determine_intent(text):
    intent_response = chat.message(f'{intents['intent_message']}\n\n{INTENT_LIST}', text)
    log.info(f'Intent: {intent_response}')
    
    return intent_response

def resolve_intent_parameters(intent_name, intent_request):
    intent_yaml_string = yaml_tools.match_yaml_pair(intents, 'name', intent_name)
    prompt = f'{intent_request}\n\n{intent_yaml_string}'
    log.info(f'Full request for action: \n\n {prompt}')

    action_response = chat.message(f"{intents['action_message']}\n\n", prompt)
    log.info(f'Action: {action_response}')

    return action_response

