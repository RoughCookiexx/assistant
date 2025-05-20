import requests
import threading

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from interface import aws_cognito
from services import command_handler
from util import logger, record_request

log = logger.setup_logger()
voice_command_blueprint = Blueprint('voice_command', __name__)


@voice_command_blueprint.route('/voice_command', methods=['POST'])
def forward_url():
    url = request.get_json().get('url')
    device_token = request.get_json().get('device_token')
    user_token = request.headers.get("Authorization")
    
    # TODO: Check out fastAPI to deal with validation:
    if not url:
        raise BadRequest('Missing parameter: url')
    if not device_token:
        raise BadRequest('Missing parameter: device_token')
    if not user_token:
        raise BadRequest('Missing parameter: user_token')

    user_token = user_token.removeprefix("Bearer ")

    if url:
        record_request.flask_request_to_curl(request, 'last_request.curl')
        thread = threading.Thread(target=command_handler.handle_command, args=(url,device_token, user_token))
        thread.start()
        return jsonify({"message": "Job started for URL: " + url})
    else:
        return jsonify({"message": "No URL provided"})

