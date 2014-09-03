import logging


__all__ = ['bridge', 'lights']

logger = logging.getLogger('hue')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
