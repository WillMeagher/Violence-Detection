from ml import model
import numpy as np
import cv2

class PredictViolence(model.Model):

    def __init__(self, models_path):
        super().__init__(models_path)
        self.frames = []


    def run(self, input):
        prediction = super().run(input)

        return prediction


    def process_prediction(self, prediction):
        prediction = prediction[0][1]

        prediction = round(prediction, 3)

        return prediction


    def prepare(self, input):
        input = np.array(input)
        input = input.reshape(1, 50, 100, 100, 3)
        input = input / 255.0
        return input


    def add_frame(self, frame):
        if len(self.frames) == 50:
            self.frames = []

        frame = cv2.resize(frame, (100, 100))
        self.frames.append(frame)

        if len(self.frames) == 50:
            prediction = self.run(self.frames)
            return prediction
        else:
            return None


    def get_frames(self):
        return self.frames
