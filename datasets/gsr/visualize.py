import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix

# ============================
#  IMPORT FROM accuracy.py
# ============================
from accuracy import load_and_prepare_data, evaluate_models

HIGH_PATH = "High_MWL"
LOW_PATH = "Low_MWL"

# ============================
#  LOAD DATA + MODELS
# ============================
print("Loading data...")
X, y = load_and_prepare_data(HIGH_PATH, LOW_PATH)

results, X_train, X_test, y_train, y_test, models = evaluate_models(X, y)

# ============================
#  START VISUALIZATION
# ============================
plt.style.use('seaborn-v0_8')

output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

print("Generating larger plots...")

# ----------------------------------------------------
# 1. Dataset distribution
# ----------------------------------------------------
plt.figure(figsize=(12, 8))
sns.countplot(x=y)
plt.title("Dataset Distribution: Low vs High MWL", fontsize=20)
plt.xticks([0, 1], ["Low MWL", "High MWL"], fontsize=14)
plt.xlabel("Class", fontsize=16)
plt.ylabel("Count", fontsize=16)
plt.tight_layout()
plt.savefig(f"{output_dir}/dataset_distribution.png")
plt.close()

# ----------------------------------------------------
# 2. PCA visualization (2D view)
# ----------------------------------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(12, 8))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap="coolwarm", alpha=0.7)
plt.title("PCA Visualization of GSR Features", fontsize=20)
plt.xlabel("PC1", fontsize=16)
plt.ylabel("PC2", fontsize=16)
cbar = plt.colorbar()
cbar.set_label("0 = Low MWL, 1 = High MWL", fontsize=14)
plt.tight_layout()
plt.savefig(f"{output_dir}/pca_plot.png")
plt.close()

# ----------------------------------------------------
# 3. Feature correlation heatmap
# ----------------------------------------------------
df = pd.DataFrame(X)

plt.figure(figsize=(14, 10))
sns.heatmap(df.corr(), cmap="coolwarm", cbar=True)
plt.title("Feature Correlation Heatmap", fontsize=20)
plt.tight_layout()
plt.savefig(f"{output_dir}/heatmap_features.png")
plt.close()

# ----------------------------------------------------
# 4. Model accuracy comparison (bar graph)
# ----------------------------------------------------
model_names = []
accuracies = []

for name, result in results.items():
    if result is not None:
        model_names.append(name)
        accuracies.append(result["accuracy"])

plt.figure(figsize=(14, 10))
sns.barplot(x=accuracies, y=model_names, palette="viridis")
plt.title("Model Test Accuracies", fontsize=20)
plt.xlabel("Accuracy", fontsize=16)
plt.ylabel("Model", fontsize=16)
plt.xlim(0, 1)
plt.tight_layout()
plt.savefig(f"{output_dir}/model_accuracies.png")
plt.close()

# ----------------------------------------------------
# 5. Confusion matrix per model
# ----------------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train2)
X_test_scaled = scaler.transform(X_test2)

for name, model in models.items():
    if name in ["SVM", "Neural Network", "K-Nearest Neighbors", "Logistic Regression"]:
        model.fit(X_train_scaled, y_train2)
        preds = model.predict(X_test_scaled)
    else:
        model.fit(X_train2, y_train2)
        preds = model.predict(X_test2)

    cm = confusion_matrix(y_test2, preds)

    plt.figure(figsize=(12, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {name}", fontsize=20)
    plt.xlabel("Predicted", fontsize=16)
    plt.ylabel("Actual", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/cm_{name.replace(' ', '_')}.png")
    plt.close()

# ----------------------------------------------------
# 6. Cross-validation boxplot
# ----------------------------------------------------
cv_data = {}

for name, result in results.items():
    if result is not None:
        cv_data[name] = result["cv_scores"]

plt.figure(figsize=(14, 10))
sns.boxplot(data=pd.DataFrame(cv_data))
plt.title("Cross-Validation Performance per Model", fontsize=20)
plt.ylabel("Accuracy", fontsize=16)
plt.xticks(rotation=45, fontsize=14)
plt.tight_layout()
plt.savefig(f"{output_dir}/cv_boxplot.png")
plt.close()

print("\nAll visualizations saved inside:")
print(f"➡ {os.path.abspath(output_dir)}")
print("\nDone!")
