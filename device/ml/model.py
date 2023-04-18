from tensorflow import keras

class Model:

    def __init__(self, models_path):
        self.model = keras.models.load_model(models_path)


    def run(self, input):
        input_data = self.prepare(input)
        prediction = self.predict(input_data)
        prediction = self.process_prediction(prediction)

        return prediction


    def predict(self, input_data):
        return self.model.predict(input_data, verbose=0)


    def prepare(self, input):
        pass


    def process_prediction(self, prediction):
        pass