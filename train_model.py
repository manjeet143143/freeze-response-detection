import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data

df = pd.read_csv("sensor_data.csv")

X = df[['movement', 'audio', 'duration']]
y = df['freeze']

# Split data

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size = 0.2)

# Train model

model = RandomForestClassifier()

model.fit(X_train, y_train)

# Accuracy

accuracy = model.score(X_test, y_test)

print("Accuracy:", accuracy)

# Save model

pickle.dump(model, open("model.pkl", "wb"))

print("Model Saved")