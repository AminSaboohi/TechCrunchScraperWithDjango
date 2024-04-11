import logging


def build_logger():
    # Set up basic configuration for logging
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', )
    logger_ = logging.getLogger()
    logger_.setLevel(logging.DEBUG)
    return logger_
