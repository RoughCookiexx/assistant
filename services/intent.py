import yaml

from action.registry import ACTION_HANDLERS
from interface import chat
from util import logger

log = logger.setup_logger()

with open('intents.yaml', 'r') as intent_file:
        intents = yaml.safe_load(intent_file)


def determine_intent(text: str) -> str:
    intent_response = chat.message(f'{intents['intent_message']}\n\n{','.join(ACTION_HANDLERS)}', text)
    log.info(f'Intent: {intent_response}')

    return intent_response

def resolve_intent_parameters(intent_name: str, intent_request: str) -> str:
    blank_action = ACTION_HANDLERS[intent_name]['model'].__annotations__
    prompt = f'{intent_request}\n\n{blank_action}'
    log.info(f'Full request for action: \n\n {prompt}')

    action_response = chat.message(f"{intents['action_message']}\n\n", prompt)
    log.info(f'Action: {action_response}')

    return action_response

