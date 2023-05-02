from picamera2 import Picamera2

class Camera:
    def __init__(self, camera_dims = (640, 360)):
        self.picam2 = Picamera2()

        camera_config = self.picam2.create_still_configuration(main={"size":camera_dims, "format": "RGB888"})
        self.picam2.configure(camera_config)

        self.picam2.start()

    def get_frame(self):
        frame = self.picam2.capture_array()
        return frame

    def release(self):
        self.picam2.stop()
