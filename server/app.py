from flask import Flask, render_template, request, redirect, url_for, Response, flash
from sys import argv
import json
import time
import logging

if len(argv) > 1:
    CONFIG = json.loads(argv[1])
else:
    print("No config")
    exit()

app = Flask(__name__)

app.secret_key = CONFIG["secret_key"]

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

frame = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x02\x01\x01\x01\x01\x01\x02\x01\x01\x01\x02\x02\x02\x02\x02\x04\x03\x02\x02\x02\x02\x05\x04\x04\x03\x04\x06\x05\x06\x06\x06\x05\x06\x06\x06\x07\t\x08\x06\x07\t\x07\x06\x06\x08\x0b\x08\t\n\n\n\n\n\x06\x08\x0b\x0c\x0b\n\x0c\t\n\n\n\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfd\xfc\xaf\xff\xd9'
last_prediction = "No prediction yet"

THIS_PATH = CONFIG["project_path"] + "server/"
DATA_FILE = THIS_PATH + 'data.json'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_frames():
    global frame
    while True:
        time.sleep(0.2)
        yield (b'--frame\r\nContent-Type: text/plain\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    data = read_data()
    return render_template('index.html', entries=data)

@app.route('/update', methods=['POST'])
def update_data():
    data = read_data()
    for key in data.keys():
        data[key] = request.form[key]
    write_data(data)
    flash('Data updated successfully! Restart the camera to see the changes.')
    return redirect(url_for('index'))

@app.route('/config')
def config_data():
    data = read_data()
    return data

@app.route('/frame', methods=['GET', 'POST'])
def frame_route():
    if request.method == 'GET':
        response = Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        global frame
        frame = request.data
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/last_prediction', methods=['GET', 'POST'])
def last_prediction_route():
    global last_prediction
    if request.method == 'GET':
        return last_prediction
    else:
        last_prediction = request.data
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')