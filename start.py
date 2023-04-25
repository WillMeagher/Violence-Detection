from subprocess import Popen
import time
import json
from config import config

def start():
    config_json = json.dumps(config)
    
    process1 = Popen(["python", config["project_path"] + "server/app.py", config_json])

    # Wait for the server to start
    time.sleep(3)

    process2 = Popen(["python", config["project_path"] + "device/run.py", config_json])

    process1.wait()
    process2.wait()

if __name__ == "__main__":
    start()