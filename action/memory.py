import boto3
import pydantic

from .action import BaseAction
from action.registry import action_handler
from interface import chat
from interface import aws_dynamo
from util import logger

from pydantic import BaseModel
from typing import Dict, List, override

log = logger.setup_logger()

class RememberAction(BaseAction):
    thing_to_remember: str

    @property
    def run_on_server(self) -> bool:
        return True

@action_handler("remember_something")
def remember_something(data: RememberAction):
    log.info(f'Thing to remember: {data.thing_to_remember}')

    # Does the table we want exist?
    table_list = aws_dynamo.list_tables()
    table_name = chat.message(f'Which of these table can we insert this request into? Return only the table name. If we must create one - return "None".',  data.thing_to_remember)
    
    # No? - Generate Create Query
    if table_name == 'None':
        dynamo_query = chat.message(f'Generate a query to create a table in DynamoDB that can record this information. Be generic. Return only the data in the following format: {CreateTableModel.__annotations__}', data.thing_to_remember)
        log.info(f"Chat Jippity created this request for Dynamo:\n\n {dynamo_query}")
        dynamo_query = dynamo_query.replace("\'", "\"")
        create_table(CreateTableModel.model_validate_json(dynamo_query))

    #   - Execute Create Query
    # Generate Insert Query
    # Execute Insert Query
    # Report results
    return "Success!"


class CreateTableModel(BaseModel):
    table_name: str
    key_schema: List[Dict[str, str]]
    attribute_definitions: List[Dict[str, str]]    

def create_table(data: CreateTableModel):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName=data.table_name,
        KeySchema=data.key_schema,
        AttributeDefinitions=data.attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    log.info(f'Table created: {data.table_name}')
