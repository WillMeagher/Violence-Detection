from ml import model
import numpy as np
import cv2
import time

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
        frame = cv2.resize(frame, (100, 100))
        self.frames.append(frame)

        if len(self.frames) == 50:
            prediction = self.run(self.frames)
            self.frames = self.frames[25:]
            return prediction
        else:
            return None
        
    
    def save_frames(self):
        frames = self.frames
        fourcc = cv2.VideoWriter_fourcc(*"XVID")

        path = "violence_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"

        out = cv2.VideoWriter(path, fourcc, 25, (frames[0].shape[1], frames[0].shape[0]))

        for frame in frames:
            out.write(frame)

        out.release()