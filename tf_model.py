import os
import sys
import tensorflow as tf
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
# import dill

#필요한 상수들
lat_min=20.467
lat_max=41.5
lon_min=120.0
lon_max=136.33
type_list=['기관이상','방향상실','부유물감김','운항저해','인명사상','전복','조난','충돌','침몰','침수','화재']


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#모델 로드
loaded_model = tf.keras.models.load_model(resource_path('accident_prediction_model.keras'))
preprocessor = joblib.load(resource_path('preprocessor.pkl'))


def acc_type_predict(latitude,longitude,ship_type,weather):
    lat_bins = np.arange(lat_min, lat_max + 0.1, 0.1)
    lon_bins = np.arange(lon_min, lon_max + 0.1, 0.1)
    lat_bin_index = np.digitize(latitude, lat_bins)
    lon_bin_index = np.digitize(longitude, lon_bins)
    region=lat_bin_index.astype(str)+'_'+lon_bin_index.astype(str)
    preprocessor_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor)
    ])
    input_data_df = pd.DataFrame({
        'Weather': [weather],
        'Ship_Type': [ship_type],
        'region': [region]
    })
    preprocessed_data = preprocessor_pipeline.transform(input_data_df)
    predictions = loaded_model.predict(preprocessed_data)
    top_3_pred_classes = np.argsort(predictions, axis=1)[:, -3:]
    top_3 = top_3_pred_classes[0][::-1]
    result=[]
    for i in range(3):
        result.append(type_list[top_3[i]])
    print("예측 결과:", result) #1,2,3위 순
    top_3_probabilities = predictions[0][top_3]
    return result, top_3_probabilities

# acc_type_predict(33.8, 125.2, '어선', '양호') -> GUI에선 이때부터 에러 생김