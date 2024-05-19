from flask import Flask, json
from flask import request
from flask_cors import CORS, cross_origin

import numpy as np
import pickle

from sklearn.feature_extraction.text import CountVectorizer


import pandas as pd

from sklearn import svm
from sklearn.model_selection import GridSearchCV

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

model_pkl_file = "models/model.pkl"
global glob_model
global glob_vectorizer


def load_model():
    with open(model_pkl_file, 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model


def create_model():
    data = pd.read_csv('./spam.csv')
    y_data = data['v1']
    x_data = data['v2']

    split = (int)(0.8 * data.shape[0])
    x_train = x_data[:split]
    x_test = x_data[split:]
    y_train = x_data[:split]
    y_test = x_data[split:]

    count_vector = CountVectorizer()
    extracted_features = count_vector.fit_transform(x_data)

    tuned_parameters = {'kernel': ['rbf', 'linear'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    model = GridSearchCV(svm.SVC(), tuned_parameters)
    model.fit(extracted_features, y_data)
    return model, count_vector

@api.route('/predict', methods=['POST'])
@cross_origin()
def predict_email_class():
    data = request.json

    string_as_array_not_clean = data['content']
    vectorized_array = glob_vectorizer.transform([string_as_array_not_clean])

    prediction = glob_model.predict(vectorized_array)
    return json.dumps([{"content": prediction[0]}])


if __name__ == '__main__':
    # model = load_model()
    glob_model, glob_vectorizer = create_model()
    api.run()
