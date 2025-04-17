from flask import Flask
from api.voice_command import voice_command_blueprint
from util import logger

app = Flask(__name__)
app.register_blueprint(voice_command_blueprint)

log = logger.setup_logger()

if __name__ == "__main__":
        log.info("Assistant launching")
        app.run(host="0.0.0.0", port=5000, debug=True)
