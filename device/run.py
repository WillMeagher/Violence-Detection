import cv2
from tools import speed_test, buffer, server, emailer# , input_check, led_controller
from camera import camera
from ml import predict_violence
from sys import argv
import time
import json

if len(argv) > 1:
    CONFIG = json.loads(argv[1])
else:
    exit()

CAMERA_WIDTH = 160
CAMERA_HEIGHT = 120

BUFFER_SECONDS = 15

MODEL_PATH = "ml/models/model.h5"
FOOTAGE_PATH = "footage/"
IMAGE_PATH = "images/frame.jpg"

PROJECT_PATH = CONFIG["project_path"] + "device/"
EXPECTED_FPS = CONFIG["expected_fps"]

GREEN_PIN = 17
# green_led = led_controller.LEDController(GREEN_PIN)

def main():
    if not server.config_set():
        print("Server config not set")
        return
    else:
        server_config = server.get_config()

    cam = camera.Camera((CAMERA_WIDTH, CAMERA_HEIGHT))
    speed_tester = speed_test.SpeedTest()
    frame_buffer = buffer.Buffer(EXPECTED_FPS * BUFFER_SECONDS)

    violence_model = predict_violence.PredictViolence(PROJECT_PATH + MODEL_PATH)

    if server_config['send_emails'] == "true":
        email = emailer.Emailer(CONFIG["emailer_email"], CONFIG["emailer_password"])

    # green_led.turn_on()

    while True:
        frame = cam.get_frame()

        frame_buffer.add(frame)
        prediction = violence_model.add_frame(frame)

        loops_per_second = speed_tester.get_loops_per_second()

        if prediction is not None:
            print(prediction)

            if prediction > float(server_config["threshold"]):
                print("Violence detected")
                
                # save frames to video file
                frames = violence_model.get_frames()
                frames_path = write_video(frames, "violence_", loops_per_second)

                # save buffer to video file
                buffer_frames = frame_buffer.get()
                buffer_path = write_video(buffer_frames, "buffer_", loops_per_second)

                if server_config['send_emails'] == "true":
                    try:
                        email.send_email(server_config["email"], "Violence Detected on " + server_config["camera_name"], "Violence detected at " + time.strftime("%Y-%m-%d_%H-%M-%S"), [buffer_path])
                    except:
                        print("Email failed to send")

        speed_tester.loop(print_loops=True)

        if server_config['send_frames'] == "true" and speed_tester.get_total_loops() % (EXPECTED_FPS * 5) == 0:
            cv2.imwrite(PROJECT_PATH + IMAGE_PATH, frame)

            with open(PROJECT_PATH + IMAGE_PATH, "rb") as f:
                r = server.post_frame(f)

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
    # input_check.exit()


def write_video(frames, name, fps):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    path = PROJECT_PATH + FOOTAGE_PATH + name + time.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"

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