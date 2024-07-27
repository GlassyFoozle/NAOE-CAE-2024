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
with open(resource_path('label_encoder.pkl'), 'rb') as f:
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

    sorted_indices = prob.argsort()[:]
    sorted_predictions = label_encoders['Accident_Type'].inverse_transform(sorted_indices)
    print(sorted_predictions)
    prob.sort()
    print(prob)
    return sorted_predictions, prob

# 예시 코드
# acc_type_predict(36.45361, 129.4353, 11, '풍랑주의보', '어선', 5)
