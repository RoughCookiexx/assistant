import requests
import threading

from flask import Flask, request, jsonify
from services import intent
from util import logger

app = Flask(__name__)
log = logger.setup_logger()


@app.route('/voice_command', methods=['POST'])
def forward_url():
    url = request.json.get('url')
    
    if url:
        thread = threading.Thread(target=intent.determine_intent, args=(url,))
        thread.start()
        return jsonify({"message": "Job started for URL: " + url})
    else:
        return jsonify({"message": "No URL provided"})

if __name__ == '__main__':
    app.run(debug=True)
