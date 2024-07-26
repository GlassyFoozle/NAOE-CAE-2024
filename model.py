import os
import sys
import joblib
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 모델 로드
loaded_model = joblib.load(resource_path('random_forest_model.sav'))
with open('label_encoder.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

def acc_type_predict(lat, lon, hour, weather, vessel, tons):
    input_data = pd.DataFrame({
        'latitude': [lat],
        'longitude': [lon],
        'Ship_Type': [vessel],
        'Tons': [tons],
        'Hour': [hour],
        'Weather': [weather]
    })

    for column in ['Weather', 'Ship_Type']:
        input_data[column] = label_encoders[column].transform(input_data[column])

    prob = loaded_model.predict_proba(input_data)[0]
    top_3_indices = prob.argsort()[-3:][::-1]
    print(top_3_indices)
    top_3_predictions = label_encoders['Accident_Type'].inverse_transform(top_3_indices)
    print(top_3_predictions)
    return top_3_predictions


acc_type_predict(35.158, 129.192, 16, '양호', '어선', 10)
