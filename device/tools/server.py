import requests

SERVER_URL = 'http://127.0.0.1:5000'

def config_set():
    return requests.get(SERVER_URL + '/config_set').json()['config_set']

def get_config():
    return requests.get(SERVER_URL + '/config').json()

def post_frame(frame):
    return requests.post(SERVER_URL + '/frame', files={'frame': frame}).json()