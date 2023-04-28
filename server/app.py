from flask import Flask, render_template, request, redirect, url_for, Response
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

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

frame = b''

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
    banner = request.args.get('banner', '')
    return render_template('index.html', entries=data, banner=banner)

@app.route('/update', methods=['POST'])
def update_data():
    data = read_data()
    for key in data.keys():
        data[key] = request.form[key]
    write_data(data)
    return redirect(url_for('index', banner='Data updated successfully! Restart the camera to see the changes.'))

@app.route('/config')
def config_data():
    data = read_data()
    return data

@app.route('/frame', methods=['GET', 'POST'])
def frame_route():
    if request.method == 'GET':
        return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        global frame
        frame = request.data
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/video_feed')
def video_feed():
    return render_template('video_feed.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')