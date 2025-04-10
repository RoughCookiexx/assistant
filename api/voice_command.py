import requests
import threading

from flask import Blueprint, request, jsonify
from services import command_handler
from util import logger

log = logger.setup_logger()
voice_command_blueprint = Blueprint('voice_command', __name__)


@voice_command_blueprint.route('/voice_command', methods=['POST'])
def forward_url():
    url = request.get_json().get('url')

    if url:
        thread = threading.Thread(target=command_handler.handle_command, args=(url,))
        thread.start()
        return jsonify({"message": "Job started for URL: " + url})
    else:
        return jsonify({"message": "No URL provided"})

