import joblib
import pandas as pd
import os

# Load model safely using absolute path
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "storage_health_model.pkl"
)

model = joblib.load(MODEL_PATH)

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

    input_df = pd.DataFrame([input_data], columns=feature_names)

    prob = model.predict_proba(input_df)[0][1]
    prediction = model.predict(input_df)[0]

    health_score = int((1 - prob) * 100)

    if prediction == 0:
        status = "Good"
    else:
        status = "Critical"

    return health_score, status
