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

