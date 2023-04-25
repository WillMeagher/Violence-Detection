from flask import Flask, render_template, request, redirect, url_for
from sys import argv
import json
import os
import time
import logging

if len(argv) > 1:
    CONFIG = json.loads(argv[1])
else:
    exit()

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

THIS_PATH = CONFIG["project_path"] + "server/"
DATA_FILE = THIS_PATH + 'data.json'
FRAME_PATH = THIS_PATH + 'static/frame.jpg'

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    data = read_data()
    entries = data.copy()
    banner = request.args.get('banner', '')
    return render_template('index.html', entries=entries, banner=banner)

@app.route('/update', methods=['POST'])
def update_data():
    data = read_data()
    for key in data.keys():
        data[key] = request.form[key]
    write_data(data)
    return redirect(url_for('index', banner='Data updated successfully! Restart the camera to see the changes.'))

@app.route('/config_set')
def config_set():
    data = read_data()
    config_set = all(data.values())
    return json.dumps({'config_set': config_set})

@app.route('/config')
def config_data():
    data = read_data()
    return data

@app.route('/latest_image')
def latest_image():
    # Generate a random query parameter to prevent caching
    timestamp = int(time.time())
    if not os.path.exists(FRAME_PATH):
        return 'No image available'
    html = '<img src=' + url_for('static', filename='frame.jpg') + '?' + str(timestamp) + ' width=400 height=400>'
    return html

@app.route('/frame', methods=['POST'])
def upload_frame():
    file = request.files['frame']
    file.save(FRAME_PATH)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')