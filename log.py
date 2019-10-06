import logging
from api.utils import coerce_to_post

LOG = True

logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('lisn')
fh = logging.FileHandler('lisn.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s]\n%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def extract_content(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    elif request.method == 'PUT':
        coerce_to_post(request)
        return request.PUT
    elif request.method == 'DELETE':
        coerce_to_post(request)
        return request.DELETE
    else:
        return dict()

def log(api):
    global logger

    if LOG == False:
        return api

    def logged_api(*args, **kwargs):
        request = args[0]
        response = api(request)
        logger.debug(
            str(request) + '\n'
            + '<request body> ' + str(dict(extract_content(request))) + '\n'
            + '<response status code> ' + str(response.status_code) + '\n'
            + '<response body> ' + str(response.content)[2:-1] + '\n')
        return response
    return logged_api