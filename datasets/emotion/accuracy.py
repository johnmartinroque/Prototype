# accuracy.py
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
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. LOAD DATA
# ============================================================
print("Loading dataset...")
df = pd.read_csv("mental_health_wearable_data.csv")

# Keep only rows where Emotional_State is Calm or Stressed
df = df[df['Emotional_State'].isin(['Calm', 'Stressed'])]

# ✅ Check class distribution
print("Class distribution after filtering:")
print(df['Emotional_State'].value_counts())

# Check if columns exist
required_cols = ['GSR_Values', 'Emotional_State']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' not found in dataset.")

# ============================================================
# 2. PREPARE FEATURES AND LABELS
# ============================================================
X = df[['GSR_Values']].values  # Use only GSR values as input
y = df['Emotional_State'].values  # Target label

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale the feature (GSR)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

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
# 4. TRAIN & EVALUATE EACH MODEL
# ============================================================
results = []

print("\n============================================================")
print("MODEL ACCURACY RESULTS (GSR → Emotional_State)")
print("============================================================")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    test_acc = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)
    
    results.append({
        "Model": name,
        "Test Accuracy": test_acc,
        "CV Mean": np.mean(cv_scores),
        "CV Std": np.std(cv_scores)
    })
    
    print(f"\n{name}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Cross-Validation Mean: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

# ============================================================
# 5. PRINT SUMMARY TABLE
# ============================================================
print("\n============================================================")
print("SUMMARY OF ALL MODELS")
print("============================================================")
summary = pd.DataFrame(results)
print(summary)

print("\n✅ Evaluation complete! Best model based on Test Accuracy:")
best = summary.loc[summary['Test Accuracy'].idxmax()]
print(best)
