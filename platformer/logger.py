import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def log(*args, **kw):
    print(*args, **kw)
