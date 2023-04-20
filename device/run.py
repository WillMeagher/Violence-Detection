import cv2
from tools import speed_test, buffer# , input_check
from camera import camera
from ml import predict_violence
from config import *
import time

CAMERA_WIDTH = 100
CAMERA_HEIGHT = 100

EXPECTED_FPS = 26
BUFFER_SECONDS = 15

def main():
    cam = camera.Camera((CAMERA_WIDTH, CAMERA_HEIGHT))
    speed_tester = speed_test.SpeedTest()
    frame_buffer = buffer.Buffer(EXPECTED_FPS * BUFFER_SECONDS)

    violence_model = predict_violence.PredictViolence(config["model_path"])

    while True:
        frame = cam.get_frame()
        frame_buffer.add(frame)

        prediction = violence_model.add_frame(frame)
        if prediction is not None:
            print(prediction)

            if prediction > .75:
                violence_model.save_frames()

                # save buffer to video file
                prior = frame_buffer.get()
                write_video(prior)

        speed_tester.loop()

        # for linux
        # if input_check.check("q"):
        #     break

        # for windows
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()

def cleanup():
    pass
    # input_check.exit()


def write_video(frames):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    path = "violence_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"

    out = cv2.VideoWriter(path, fourcc, EXPECTED_FPS, (frames[0].shape[1], frames[0].shape[0]))

    for frame in frames:
        out.write(frame)

    out.release()


if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()