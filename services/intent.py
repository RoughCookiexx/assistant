import yaml

from action.registry import ACTION_HANDLERS
from interface import chat
from util import logger

log = logger.setup_logger()

with open('prompts.yaml', 'r') as prompt_file:
        prompts = yaml.safe_load(prompt_file)


def determine_intent(text: str) -> str:
    intent_response = chat.message(f'{prompts['determine_intent']}\n\n{','.join(ACTION_HANDLERS)}', text)
    log.info(f'Intent: {intent_response}')

    return intent_response

def resolve_intent_parameters(intent_name: str, intent_request: str, user_id: str) -> str:
    blank_model = ACTION_HANDLERS[intent_name]['model'].__annotations__
    system_prompt = prompts['resolve_params'].format(user_id=user_id, model=blank_model)

    action_model = chat.message(system_prompt, intent_request)
    log.info(f'Action model: {action_model}')

    return action_model 

