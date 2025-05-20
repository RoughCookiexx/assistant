import boto3

def list_tables():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    tables = []
    last_evaluated_table_name = None

    while True:
        if last_evaluated_table_name:
            response = dynamodb.list_tables(ExclusiveStartTableName=last_evaluated_table_name)
        else:
            response = dynamodb.list_tables()

        tables.extend(response.get('TableNames', []))

        last_evaluated_table_name = response.get('LastEvaluatedTableName')
        if not last_evaluated_table_name:
            break

    return tables

def describe_table(table_name):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    response = dynamodb.describe_table(TableName=table_name)
    table = response['Table']
    return table['KeySchema'], table['AttributeDefinitions']

def insert_item(table_name, item):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )

def create_table(table_name, key_schema, attribute_definitions):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName=table_name.lower(),
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


