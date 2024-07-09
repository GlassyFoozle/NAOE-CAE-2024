import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.inspection import permutation_importance
from matplotlib import pyplot as plt

# 관공선, 유도선 날림
df = pd.read_csv('통합v4.csv',encoding='cp949')

# 범주형 변수들 encoding
label_encoders = {}
for column in ['Station', 'Location', 'Weather', 'Vessel_type', 'Accident_type']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

X = df[['Station', 'Location', 'Weather', 'Latitude', 'Longitude', 'Vessel_type', 'Tons', 'Month', 'Hour']]
y = df['Accident_type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=300, min_samples_leaf=4, random_state=42)
model.fit(X_train, y_train)

y_prob = model.predict_proba(X_test)

feature_names = list(X_train.columns.values)
r = permutation_importance(model, X_test, y_test, n_repeats=30)
features = dict()

for i in r.importances_mean.argsort()[::-1]:
    if r.importances_mean[i] - 2 * r.importances_std[i] > 0:
        features[X.columns[i]] = r.importances[i]
        print(f"{X.columns[i]:<8}\t"
              f"{r.importances_mean[i]:.3f}"
              f" +/- {r.importances_std[i]:.3f}")

plt.barh(feature_names, model.feature_importances_)
plt.show()

# top 3 사고
top_3_predictions = [model.classes_[proba.argsort()[-3:][::-1]] for proba in y_prob]
correct_in_top_3 = [y_test.iloc[i] in top_3 for i, top_3 in enumerate(top_3_predictions)]
accuracy_top_3 = sum(correct_in_top_3) / len(correct_in_top_3)


y_pred = model.predict(X_test)
print("Accuracy (Top 1):", accuracy_score(y_test, y_pred))
print("Accuracy (Top 3):", accuracy_top_3)
print("Classification Report (Top 1):")
print(classification_report(y_test, y_pred))


def recommend_top_3_accident_types(Station, Location, Weather, Latitude, Longitude, Vessel_type, Tons, Month, Hour):
    input_data = pd.DataFrame({
        'Station': [Station],
        'Location': [Location],
        'Weather': [Weather],
        'Latitude': [Latitude],
        'Longitude': [Longitude],
        'Vessel_type': [Vessel_type],
        'Tons': [Tons],
        'Month': [Month],
        'Hour': [Hour]
    })

    for column in ['Station', 'Location', 'Weather', 'Vessel_type']:
        input_data[column] = label_encoders[column].transform(input_data[column])

    prob = model.predict_proba(input_data)[0]
    top_3_indices = prob.argsort()[-3:][::-1]
    top_3_predictions = label_encoders['Accident_type'].inverse_transform(top_3_indices)
    return top_3_predictions

# 예시 조건
sample_station = '부산'
sample_location = '항계 내'
sample_weather = '양호'
sample_latitude = 35
sample_longitude = 128
sample_Vessel_type = '어선'
sample_tonnage = 10
sample_month = 1
sample_hour = 11

recommended_accident_types = recommend_top_3_accident_types(sample_station, sample_location, sample_weather, sample_latitude, sample_longitude, sample_Vessel_type, sample_tonnage, sample_month, sample_hour)
print("Top 3 Probable Accident Types:", recommended_accident_types)
