import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.model_selection import GridSearchCV


model_pkl_file = "models/model.pkl"


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
    with open(model_pkl_file, 'wb') as file:
        pickle.dump(model, file)



if __name__ == '__main__':
    create_model()