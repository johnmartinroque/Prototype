# accuracy.py HAPPY SAD ANGRY NEUTRAL
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings('ignore')

# ==============================
# Load and prepare the dataset
# ==============================
def load_heart_rate_data(filepath, sample_size=57268):
    """
    Load heart rate and emotion data from CSV.
    Keep only happy, sad, angry, and neutral classes.
    Optionally sample a smaller subset for faster testing.
    """
    df = pd.read_csv(filepath)

    if 'HeartRate' not in df.columns or 'Emotion' not in df.columns:
        raise ValueError("CSV must contain 'HeartRate' and 'Emotion' columns")

    # ✅ Filter only desired emotions
    allowed_emotions = ['happy', 'sad', 'angry', 'neutral']
    df = df[df['Emotion'].isin(allowed_emotions)].reset_index(drop=True)

    print(f"✅ Filtered dataset to {len(df)} rows with emotions: {allowed_emotions}")

    # Sample only a subset if dataset is large
    if sample_size is not None and len(df) > sample_size:
        print(f"Dataset has {len(df)} rows — sampling {sample_size} for faster evaluation.")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    else:
        print(f"Dataset has {len(df)} rows — using all samples.")

    X = df[['HeartRate']].values
    y = df['Emotion'].values

    # Encode emotions as numeric labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print("Emotion Classes:", list(label_encoder.classes_))
    return X, y_encoded, label_encoder


# ==============================
# Evaluate ML Models
# ==============================
def evaluate_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(kernel='linear', random_state=42, max_iter=10000),
        'Random Forest': RandomForestClassifier(random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'Neural Network': MLPClassifier(random_state=42, max_iter=1000)
    }

    results = {}

    print("\nModel Evaluation Results:")
    print("=" * 60)

    for name, model in models.items():
        try:
            if name in ['SVM', 'K-Nearest Neighbors', 'Neural Network']:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                cv_scores = cross_val_score(model, scaler.transform(X), y, cv=3)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                cv_scores = cross_val_score(model, X, y, cv=3)

            accuracy = accuracy_score(y_test, y_pred)
            mean_cv = np.mean(cv_scores)
            std_cv = np.std(cv_scores)

            results[name] = {
                'accuracy': accuracy,
                'cv_mean': mean_cv,
                'cv_std': std_cv,
                'model': model
            }

            print(f"\n{name}:")
            print(f"  Test Accuracy: {accuracy:.4f}")
            print(f"  CV Mean: {mean_cv:.4f} (+/- {std_cv * 2:.4f})")

        except Exception as e:
            print(f"\n{name} - Error: {e}")
            results[name] = None

    return results, scaler


# ==============================
# Detailed Best Model Report
# ==============================
def print_best_model_report(results, X, y, scaler, label_encoder):
    valid_results = [(name, res) for name, res in results.items() if res is not None]
    if not valid_results:
        print("No valid models to evaluate.")
        return

    best_model_name, best_result = max(valid_results, key=lambda x: x[1]['accuracy'])
    best_model = best_result['model']

    print("\n" + "=" * 60)
    print("DETAILED ANALYSIS")
    print("=" * 60)
    print(f"\nBest Model: {best_model_name}")
    print(f"Best Test Accuracy: {best_result['accuracy']:.4f}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if best_model_name in ['SVM', 'K-Nearest Neighbors', 'Neural Network']:
        best_model.fit(X_train_scaled, y_train)
        y_pred = best_model.predict(X_test_scaled)
    else:
        best_model.fit(X_train, y_train)
        y_pred = best_model.predict(X_test)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


# ==============================
# Main Execution
# ==============================
if __name__ == "__main__":
    filepath = "heart_rate_emotion_dataset.csv"

    print("Loading dataset...")
    X, y, label_encoder = load_heart_rate_data(filepath, sample_size=57268)
    print(f"Loaded {len(X)} samples for evaluation.")

    results, scaler = evaluate_models(X, y)
    print_best_model_report(results, X, y, scaler, label_encoder)

    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Model':<25} {'Test Accuracy':<15} {'CV Mean':<10} {'CV Std':<10}")
    print("-" * 60)
    for name, res in results.items():
        if res is not None:
            print(f"{name:<25} {res['accuracy']:<15.4f} {res['cv_mean']:<10.4f} {res['cv_std']:<10.4f}")

    print("\n✅ Model evaluation completed.")
