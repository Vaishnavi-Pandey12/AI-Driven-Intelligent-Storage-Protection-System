"""
Model Evaluation Script
Loads the trained model and evaluates its performance on the dataset
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)
from sklearn.model_selection import train_test_split

# Load the trained model
print("Loading model...")
model = joblib.load("models/storage_health_model.pkl")
print(f"Model type: {type(model).__name__}")
print(f"Model: {model}\n")

# Load the dataset
print("Loading dataset...")
data = pd.read_csv("data/storage_health_dataset.csv")
print(f"Dataset shape: {data.shape}")
print(f"Dataset columns: {list(data.columns)}\n")

# Check class distribution
print("Class Distribution:")
print(data['label'].value_counts())
print(f"Class 0 (Good): {(data['label'] == 0).sum()} ({(data['label'] == 0).sum() / len(data) * 100:.2f}%)")
print(f"Class 1 (Critical): {(data['label'] == 1).sum()} ({(data['label'] == 1).sum() / len(data) * 100:.2f}%)\n")

# Prepare features and labels
X = data.drop('label', axis=1)
y = data['label']

# Split into train and test sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}\n")

# Make predictions
print("Making predictions...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate metrics
print("=" * 60)
print("MODEL PERFORMANCE METRICS")
print("=" * 60)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\nAccuracy:  {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
print(f"Recall:    {recall:.4f} ({recall * 100:.2f}%)")
print(f"F1-Score:  {f1:.4f} ({f1 * 100:.2f}%)")
print(f"ROC-AUC:   {roc_auc:.4f} ({roc_auc * 100:.2f}%)")

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)
cm = confusion_matrix(y_test, y_pred)
print("\n                Predicted")
print("              Good  Critical")
print(f"Actual Good     {cm[0][0]:4d}    {cm[0][1]:4d}")
print(f"       Critical {cm[1][0]:4d}    {cm[1][1]:4d}")

# Calculate additional metrics from confusion matrix
tn, fp, fn, tp = cm.ravel()
specificity = tn / (tn + fp)
print(f"\nTrue Negatives:  {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives:  {tp}")
print(f"Specificity:     {specificity:.4f} ({specificity * 100:.2f}%)")

print("\n" + "=" * 60)
print("DETAILED CLASSIFICATION REPORT")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=['Good', 'Critical']))

# Feature importance (if available)
if hasattr(model, 'feature_importances_'):
    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop features contributing to predictions:")
    for idx, row in feature_importance.iterrows():
        print(f"{row['feature']:30s}: {row['importance']:.4f} ({row['importance'] * 100:.2f}%)")

# Test on training set to check for overfitting
print("\n" + "=" * 60)
print("OVERFITTING CHECK")
print("=" * 60)
y_train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Training Accuracy: {train_accuracy:.4f} ({train_accuracy * 100:.2f}%)")
print(f"Test Accuracy:     {accuracy:.4f} ({accuracy * 100:.2f}%)")
print(f"Difference:        {abs(train_accuracy - accuracy):.4f} ({abs(train_accuracy - accuracy) * 100:.2f}%)")

if abs(train_accuracy - accuracy) < 0.05:
    print("✓ Model is well-balanced (low overfitting)")
elif abs(train_accuracy - accuracy) < 0.10:
    print("⚠ Slight overfitting detected")
else:
    print("✗ Significant overfitting detected")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"\n✓ Model Accuracy: {accuracy * 100:.2f}%")
print(f"✓ Model can correctly identify storage health in {accuracy * 100:.1f}% of cases")
print(f"✓ False Alarm Rate: {fp / (fp + tn) * 100:.2f}% (predicts critical when actually good)")
print(f"✓ Miss Rate: {fn / (fn + tp) * 100:.2f}% (predicts good when actually critical)")

if accuracy >= 0.95:
    print("\n🌟 Excellent model performance!")
elif accuracy >= 0.90:
    print("\n✓ Very good model performance")
elif accuracy >= 0.85:
    print("\n✓ Good model performance")
elif accuracy >= 0.80:
    print("\n⚠ Acceptable model performance, consider improvements")
else:
    print("\n✗ Model needs improvement")

print("\n" + "=" * 60)
