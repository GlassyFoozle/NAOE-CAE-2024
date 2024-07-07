import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Read the CSV file
df = pd.read_csv('통합v4.csv',encoding='cp949')

# Ensure columns are named correctly: 'weather', 'latitude', 'longitude', 'ship_type', 'tonnage', 'month', 'hour', 'accident_type'
# Encode categorical data
label_encoders = {}
for column in ['Weather', 'Vessel_type', 'Accident_type']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Features and target variable
X = df[['Weather', 'Latitude', 'Longitude', 'Vessel_type', 'Tons', 'Month', 'Hour']]
y = df['Accident_type']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Hyperparameter tuning using Grid Search
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_leaf': [1, 5, 10]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_scaled, y_train)

# Best parameters found by Grid Search
print("Best Parameters:", grid_search.best_params_)

# Evaluate the model with best parameters
best_rf = grid_search.best_estimator_
y_pred = best_rf.predict(X_test_scaled)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))


# Function to recommend top 3 accident types with probabilities
def recommend_top_3_accident_types(weather, latitude, longitude, ship_type, tonnage, month, hour):
    input_data = pd.DataFrame({
        'weather': [weather],
        'latitude': [latitude],
        'longitude': [longitude],
        'ship_type': [ship_type],
        'tonnage': [tonnage],
        'month': [month],
        'hour': [hour]
    })

    for column in ['weather', 'ship_type']:
        input_data[column] = label_encoders[column].transform(input_data[column])

    input_data_scaled = scaler.transform(input_data)

    prob = best_rf.predict_proba(input_data_scaled)[0]
    top_3_indices = prob.argsort()[-3:][::-1]
    top_3_predictions = label_encoders['accident_type'].inverse_transform(top_3_indices)
    top_3_probabilities = prob[top_3_indices]

    return top_3_predictions, top_3_probabilities


# Test the recommendation function
sample_weather = '양호'
sample_latitude = 35
sample_longitude = 128
sample_ship_type = '어선'
sample_tonnage = 10
sample_month = 1  # January
sample_hour = 11  # 2 PM

recommended_accident_types, probabilities = recommend_top_3_accident_types(sample_weather, sample_latitude,
                                                                           sample_longitude, sample_ship_type,
                                                                           sample_tonnage, sample_month, sample_hour)
print("Top 3 Recommended Accident Types:", recommended_accident_types)
print("Probabilities:", probabilities)
