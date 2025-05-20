import boto3
import json
import jwt
import os
import requests
from werkzeug.exceptions import Unauthorized

from util import logger

log = logger.setup_logger()


def get_user_id(user_token: str) -> str:
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.get_user(
        AccessToken=user_token
    )

    if not response['UserAttributes']:
        raise ValueError('Auth response missing user ID')
    
    user_id = next((attribute['Value'] for attribute in response['UserAttributes'] if attribute.get('Name') == 'sub'), None)

    if user_id is None:
        raise Unauthorized("User token is invalid")

    return user_id

