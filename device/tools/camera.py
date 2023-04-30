import cv2

class Camera:
    def __init__(self, camera_dims = (640, 360), cap_id = 0):
        self.cap_id = cap_id
        self.cap = cv2.VideoCapture(self.cap_id)

        camera_x, camera_y = camera_dims

        self.cap.set(3, camera_x)
        self.cap.set(4, camera_y)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()