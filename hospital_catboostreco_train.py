
import pandas as pd
import json
from catboost import CatBoostRegressor

# Load the data from the JSON file
with open('hospital_catboost_traindata3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to pandas DataFrame
df = pd.json_normalize(data['recommendation_data'])

# Define features (X) and target (y)
features = ['distance_m', 'rating', 'congestion_level']
target = 'recommendation_score'

X = df[features]
y = df[target]

# Initialize and train the CatBoost model
# Note: For a real-world scenario, you would split the data into training and testing sets.
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = CatBoostRegressor(iterations=1000,
                          learning_rate=0.1,
                          depth=6,
                          loss_function='RMSE',
                          verbose=100)

# For this example, we train on the entire dataset
model.fit(X, y)

# Save the trained model
model.save_model('catboost_model.bin')

print("CatBoost model has been trained and saved as 'catboost_model.bin'")
