import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def log(*args, level=logging.DEBUG, **kw):
    print(*args, **kw)
