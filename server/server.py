from flask import Flask, json
from flask import request
from flask_cors import CORS, cross_origin

import pickle


api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

model_pkl_file = "models/model.pkl"
vectorizer_pkl_file = "models/vectorizer_model.pkl"
global glob_model
global glob_vectorizer


def load_model():
    with open(model_pkl_file, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model


def load_vectorizer():
    with open(vectorizer_pkl_file, 'rb') as file:
        loaded_vectorizer = pickle.load(file)
    return loaded_vectorizer


@api.route('/predict', methods=['POST'])
@cross_origin()
def predict_email_class():
    data = request.json

    string_as_array_not_clean = data['content']
    vectorized_array = glob_vectorizer.transform([string_as_array_not_clean])

    prediction = glob_model.predict(vectorized_array)
    return json.dumps({"content": prediction[0]})


if __name__ == '__main__':
    glob_model = load_model()
    glob_vectorizer = load_vectorizer()
    api.run()
