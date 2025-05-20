import json
import pydantic
import time
import yaml

from .action import BaseAction
from action.registry import action_handler
from interface import chat
from interface import aws_dynamo
from util import logger

from pydantic import BaseModel
from typing import Dict, List, override

log = logger.setup_logger()

with open('prompts.yaml', 'r') as prompt_file:
        prompts = yaml.safe_load(prompt_file)

class RememberAction(BaseAction):
    thing_to_remember: str
    user_id: str

    @property
    def run_on_server(self) -> bool:
        return True

@action_handler("remember_something")
def remember_something(data: RememberAction):
    log.info(f'Thing to remember: {data.thing_to_remember}')

    # Does the table we want exist?
    table_list = aws_dynamo.list_tables()
    table_name = chat.message(
        prompts['determine_table'].format(table_list=','.join(table_list)),
        data.thing_to_remember)
    log.info(f'Chat Jippity thinks we should use table: {table_name}')
    
    # No? - Create Table
    if table_name.lower() == 'none':
        create_query = chat.message(prompts['generate_table'].format(annotations=CreateTableModel.__annotations__), data.thing_to_remember)
        log.info(f"Chat Jippity created this request for Dynamo:\n\n {create_query}")
        create_query = create_query.replace("\'", "\"")
        create_model = CreateTableModel.model_validate_json(create_query)
        aws_dynamo.create_table(create_model.table_name, create_model.key_schema, create_model.attribute_definitions)
        log.info(f'Table created: {table_name}')
        table_name = create_model.table_name.lower()

    # Generate Insert Query
    key_schema, attribute_definitions = aws_dynamo.describe_table(table_name)
    item_json = chat.message(prompts['generate_insert'].format(table_name=table_name, 
            key_schema=key_schema, 
            attribute_definitions=attribute_definitions,
            time=time.time(),
            user_id=data.user_id),
            data.thing_to_remember)
    log.info(f'Chat Jippity want to insert this item: \n{item_json}\n')

    # Execute Insert Query
    item = json.loads(item_json)
    aws_dynamo.insert_item(table_name, item)

    # Report results
    return f'Entered {item_json} into table {table_name}'


class CreateTableModel(BaseModel):
    table_name: str
    key_schema: List[Dict[str, str]]
    attribute_definitions: List[Dict[str, str]]    

