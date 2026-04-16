import json
import pickle
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    # Use the model dir path relative to backend
    model_dir = os.path.join(os.path.dirname(__file__), 'model')
    features_path = os.path.join(model_dir, 'features.json')
    model_path = os.path.join(model_dir, 'bangalore_model.pkl')

    with open(features_path, "r") as f:
        data = json.load(f)
        __data_columns = [col.lower() for col in data['features']]
        __locations = __data_columns[3:]

    if __model is None:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)

def get_location_names():
    if __locations is None:
        load_saved_artifacts()
    return __locations
