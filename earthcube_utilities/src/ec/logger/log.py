import logging, os, sys
from logging import Logger
def config_notebook() -> Logger:
    """Use this to get default logging behavior while in a notebook"""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"),
                        stream=sys.stdout)
    log = logging.getLogger()
    return log

def config_app() -> Logger:
    """Use this to set default logging behavior while in a console application"""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"),
                        stream=sys.stdout)
    log = logging.getLogger()
    return log

def config_web() -> Logger:
    """Use this to set default logging behavior a web applicaiton like Flask"""
    logging.basicConfig(format='%(levelname)s : %(message)s', level=os.environ.get("LOGLEVEL", "INFO"),
                        stream=sys.stdout)
    log = logging.getLogger()
    return log