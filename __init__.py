from flask import Flask
from api import voice_command
from util import logger

app = Flask(__name__)
log = logger.setup_logger()

if __name__ == "__main__":
        log.info("Assistant launching")
        app.run(debug=True)
