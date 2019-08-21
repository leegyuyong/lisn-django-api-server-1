import logging

logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('lisn')

fh = logging.FileHandler('lisn.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)