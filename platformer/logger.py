import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log(*args, level=logging.DEBUG, **kw):
    if level >= logger.level:
        print(*args, **kw)
