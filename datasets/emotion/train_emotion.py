# train_emotion.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. LOAD DATA
# ============================================================
print("📂 Loading dataset...")
df = pd.read_csv("mental_health_wearable_data.csv")

# Keep only Calm and Stressed
df = df[df['Emotional_State'].isin(['Calm', 'Stressed'])]
print("Class distribution after filtering:")
print(df['Emotional_State'].value_counts())

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

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale GSR values
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================
# 3. DEFINE MODELS
# ============================================================
models = {
    "Logistic Regression": LogisticRegression(),
    "SVM (RBF Kernel)": SVC(kernel='rbf', probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Neural Network (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
}

# ============================================================
# 4. TRAIN & SELECT BEST MODEL
# ============================================================
results = []
best_acc = 0
best_model = None
best_name = ""

print("\n============================================================")
print("TRAINING MODELS (GSR → Calm/Stressed)")
print("============================================================")

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    test_acc = accuracy_score(y_test, y_pred)
    results.append((name, model, test_acc, y_pred))
    
    print(f"\n{name}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    if test_acc > best_acc:
        best_acc = test_acc
        best_model = model
        best_name = name

# ============================================================
# 5. SAVE BEST MODEL AND SCALER
# ============================================================
print("\n💾 Saving best model and scaler...")
joblib.dump(best_model, "best_model_emotion.pkl")
joblib.dump(scaler, "scaler_emotion.pkl")

print("\n✅ Training complete!")
print(f"Best model: {best_name} with Test Accuracy: {best_acc:.4f}")
print("Saved files:")
print(" - best_model_emotion.pkl")
print(" - scaler_emotion.pkl")
