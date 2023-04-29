from ml import model
import numpy as np
import cv2

class PredictViolence(model.Model):

    def __init__(self, models_path):
        super().__init__(models_path)
        self.flow = []
        self.last_frame = None
        self.last_prediction = 0.0


    def run(self, input):
        prediction = super().run(input)

        return prediction


    def process_prediction(self, prediction):
        prediction = prediction[0][1]

        prediction = round(prediction, 3)
        self.last_prediction = prediction

        return prediction


    def prepare(self, input):
        input = np.array(input)
        input = input.reshape(1, 50, 100, 100, 3)
        input = input / 255.0
        return input


    def add_frame(self, frame):
        if len(self.flow) == 50:
            self.flow = []
            self.last_frame = None

        frame = cv2.resize(frame, (100, 100))

        if self.last_frame is not None:
            flow = self.last_frame - frame
            self.flow.append(flow)

        self.last_frame = frame

        if len(self.flow) == 50:
            prediction = self.run(self.flow)
            return prediction
        else:
            return None

    def get_last_prediction(self):
        return self.last_prediction