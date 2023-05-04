import cv2
from tools import speed_test, buffer, server, emailer, camera# , input_check, led_controller, picamera
from ml import predict_violence
from sys import argv
import time
import json
import os

if len(argv) > 1:
    CONFIG = json.loads(argv[1])
else:
    print("No config")
    exit()

CAMERA_WIDTH = 100
CAMERA_HEIGHT = 100

BUFFER_SECONDS = 15

MODEL_PATH = "ml/models/model.h5"
FOOTAGE_PATH = "footage/"
IMAGE_PATH = "images/frame.jpg"

PROJECT_PATH = CONFIG["project_path"] + "device/"
EXPECTED_FPS = CONFIG["expected_fps"]

GREEN_PIN = 27

send_email_file = None
# green_led = led_controller.LEDController(GREEN_PIN)

def main():
    server_config = server.get_config()
    if not all(server_config.values()):
        print("Server config not set")
        return
    
    camera_rotation = int(server_config["camera_rotation"])
    image_rotation = None
    if camera_rotation == 90:
        image_rotation = cv2.ROTATE_90_COUNTERCLOCKWISE
    elif camera_rotation == 180:
        image_rotation = cv2.ROTATE_180
    elif camera_rotation == 270:
        image_rotation = cv2.ROTATE_90_CLOCKWISE

    cam = camera.Camera((CAMERA_WIDTH, CAMERA_HEIGHT))
    # cam = picamera.Camera((CAMERA_WIDTH, CAMERA_HEIGHT))
    speed_tester = speed_test.SpeedTest()
    frame_buffer = buffer.Buffer(EXPECTED_FPS * BUFFER_SECONDS)

    violence_model = predict_violence.PredictViolence(PROJECT_PATH + MODEL_PATH)

    if server_config['send_emails'] == "true":
        email = emailer.Emailer(CONFIG["emailer_email"], CONFIG["emailer_password"])

    # green_led.turn_on()

    while True:
        frame = cam.get_frame()

        if image_rotation is not None:
            frame = cv2.rotate(frame, image_rotation)

        frame_buffer.add(frame)
        prediction = violence_model.add_frame(frame)

        loops_per_second = speed_tester.get_loops_per_second()

        if prediction is not None:
            print(prediction)

            if prediction > float(server_config["threshold"]):
                print("Violence detected")
                
                # save buffer to video file
                buffer_frames = frame_buffer.get()
                file_name = "Violence_Detected_on_Camera_" + server_config["camera_name"].replace(" ", "_") + "_at_" + time.strftime("%Y-%m-%d_%H-%M-%S")
                buffer_path = write_video(buffer_frames, file_name, loops_per_second)
                if server_config['send_emails'] == "true":
                    send_email_file = buffer_path

        if send_email_file is not None:
            if os.path.exists(send_email_file):
                try:
                    subject = "Violence Detected on " + server_config["camera_name"]
                    body = "Violence detected on camera " + server_config["camera_name"] + " at " + time.strftime("%Y-%m-%d_%H-%M-%S")
                    email.send_email(server_config["email"], subject, body, [buffer_path])
                    send_email_file = None
                except:
                    print("Email failed to send")

        speed_tester.loop(print_loops=True)

        if server_config['send_frames'] == "true" and speed_tester.get_total_loops() % max(int(EXPECTED_FPS / 5), 1) == 0:
            encoded_img = cv2.imencode('.jpg',frame)[1]
            img_string = encoded_img.tobytes()
            server.send_frame(img_string)

        last_prediction = str(violence_model.get_last_prediction())
        server.send_prediction(last_prediction)

        # for linux
        # if input_check.check("q"):
        #     break

        # for windows
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()


def cleanup():
    pass
    # green_led.turn_off()
    # green_led.cleanup()
    # input_check.exit()


def write_video(frames, name, fps):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    path = PROJECT_PATH + FOOTAGE_PATH + name + ".mp4"

    out = cv2.VideoWriter(path, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)

    out.release()

    return path

# add a config parameter to the main
if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()