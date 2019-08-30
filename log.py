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

def log(request, status_code, request_param='None', json_res='None'):
    global logger
    logger.debug(str(request) + '\n' + str(request_param) + '\n' + str(json_res) + '\n' + 'status=' + str(status_code) + '\n')