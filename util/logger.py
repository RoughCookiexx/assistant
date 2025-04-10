import logging

class Logger:
    _instance = None

    def __init__(self):
        self.log = logging.getLogger()
        self.setup()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setup(self):
        if len(self.log.handlers) > 0: 
            return self.log

        self.log.setLevel(logging.INFO)

        # Create a file handler
        file_handler = logging.FileHandler('log_file.log')
        file_handler.setLevel(logging.INFO)

        # Create a formatter and set the format for the log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the self.log
        self.log.addHandler(file_handler)

        return self.log


def setup_logger():
    # Create a logger
    return Logger().log
    
