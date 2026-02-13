import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
df = pd.read_csv("storage_health_dataset.csv")

# Features and target
X = df.drop("label", axis=1)
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/storage_health_model.pkl")

print("\nModel saved successfully.")

import joblib
import pandas as pd

# Load model
model = joblib.load("models/storage_health_model.pkl")

feature_names = [
    "disk_usage_percent",
    "temperature",
    "read_error_rate",
    "write_error_rate",
    "reallocated_sector_count",
    "pending_sector_count",
    "power_on_hours"
]

def predict_health(input_data):

    # Convert to DataFrame with correct column names
    input_df = pd.DataFrame([input_data], columns=feature_names)

    prob = model.predict_proba(input_df)[0][1]  # failure probability
    prediction = model.predict(input_df)[0]

    health_score = int((1 - prob) * 100)

    if prediction == 0:
        status = "Good"
    else:
        status = "Critical"

    return health_score, status

if __name__ == "__main__":
    sample_input = [40, 30, 10, 12, 5, 3, 5000]

    score, status = predict_health(sample_input)

    print("\nHealth Score:", score)
    print("Status:", status)

