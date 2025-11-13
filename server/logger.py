import logging

def logger_setup(name="myRag"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] --- [%(message)s]")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger

# checking

logger = logger_setup()

logger.debug("debugging")
logger.info("process started")
logger.error("error")
logger.critical("Critical")

