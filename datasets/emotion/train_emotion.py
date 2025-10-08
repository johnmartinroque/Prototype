# train_emotion.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. LOAD DATA
# ============================================================
print("📂 Loading dataset...")
df = pd.read_csv("mental_health_wearable_data.csv")

# Required columns
required_cols = ['GSR_Values', 'Emotional_State']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' not found in dataset.")

# ============================================================
# 2. PREPARE FEATURES AND LABELS
# ============================================================
X = df[['GSR_Values']].values  # only GSR
y = df['Emotional_State'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale GSR values
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================
# 3. TRAIN MODEL
# ============================================================
print("⚙️ Training Logistic Regression model...")
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# ============================================================
# 4. EVALUATE MODEL
# ============================================================
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)

print("\n============================================================")
print("MODEL EVALUATION")
print("============================================================")
print(f"✅ Test Accuracy: {acc:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ============================================================
# 5. SAVE MODEL AND SCALER
# ============================================================
print("\n💾 Saving trained model and scaler...")
joblib.dump(model, "best_model_emotion.pkl")
joblib.dump(scaler, "scaler_emotion.pkl")

print("\n✅ Model training complete! Files saved:")
print(" - best_model_emotion.pkl")
print(" - scaler_emotion.pkl")
