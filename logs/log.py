import logging
from logging import Logger
import sys
import socket
from logging.handlers import SysLogHandler, TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s: %(lineno)d - %(levelname)s - %(message)s")
paper_trail_format = "%(asctime)s %(hostname)s %(funcName)s %(lineno)d : %(message)s"
paper_trail_format = logging.Formatter(paper_trail_format, datefmt="%b %d %H:%M:%S")

LOG_FILE = "my_app.log"



class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True
    

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler

def get_papertail_handler():
    papertail_handler = SysLogHandler(address=("logs2.papertrailapp.com", 15222))
    papertail_handler.addFilter(ContextFilter())
    papertail_handler.setFormatter(paper_trail_format)
    return papertail_handler



def get_logger(logger_name, to_console=False) -> logging.Logger:
    
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    
    
    
    logger.addHandler(get_file_handler())
    logger.addHandler(get_file_handler())
    logger.addHandler(get_papertail_handler())

    if to_console:
        logger.addHandler(get_console_handler())
    
    logger.propagate = False

    return logger