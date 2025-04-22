import boto3

from botocore.exceptions import ClientError
from util import logger

log = logger.setup_logger()

def push(endpoint_id, key, value):
    pinpoint = boto3.client('pinpoint', region_name='us-east-1')
    application_id = '71926f5c6f1940d19377d188250ab7f6'

    # Define the message to be sent in the notification
    message = {
        'Action': 'DEEP_LINK',
        'Data': {
            key: value
        },
        'Title': 'YO',
        'Body': 'Your Buttler is trying to get in touch with you.'
    }

    # Send the notification
    try:
       response = pinpoint.send_messages(
            ApplicationId=application_id,
            MessageRequest={
                'Addresses': {
                    endpoint_id: {
                        'ChannelType': 'GCM'
                    }
                },
                'MessageConfiguration': {
                    'GCMMessage': {
                        'Action': message['Action'],
                        'Data': message['Data'],
                        'Title': message['Title'],
                        'Body': message['Body'],
                        'Url': 'app://open.my.app'
                    }
                }
            }
        )
    except ClientError:
        log.error('Pinpoint failed to send message.')


