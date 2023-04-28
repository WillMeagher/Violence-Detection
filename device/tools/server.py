import requests

SERVER_URL = 'http://127.0.0.1:5000'

def get_config():
    return requests.get(SERVER_URL + '/config').json()

def send_frame(frame):
    return requests.post(SERVER_URL + '/frame', data=frame)