import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import warnings
import joblib

warnings.filterwarnings('ignore')

# Paths for PPG data
high_path = "High_MWL"
low_path = "Low_MWL"


def load_and_prepare_data(high_path, low_path):
    """
    Load PPG data from High_MWL and Low_MWL folders and prepare features/labels.
    Each CSV is flattened into a 1D feature vector.
    """
    X, y = [], []

    # Load High MWL PPG files (p2h.csv to p25h.csv)
    for i in range(2, 26):
        filename = f"p{i}h.csv"
        filepath = os.path.join(high_path, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath, header=None)
                df = df.apply(pd.to_numeric, errors='coerce').dropna()
                if not df.empty:
                    # Flatten the signal data into a feature vector
                    features = df.values.flatten()
                    X.append(features)
                    y.append(1)  # High MWL = 1
                    print(f"Loaded High MWL PPG: {filename}, Features: {len(features)}")
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    # Load Low MWL PPG files (p2l.csv to p25l.csv)
    for i in range(2, 26):
        filename = f"p{i}l.csv"
        filepath = os.path.join(low_path, filename)
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath, header=None)
                df = df.apply(pd.to_numeric, errors='coerce').dropna()
                if not df.empty:
                    features = df.values.flatten()
                    X.append(features)
                    y.append(0)  # Low MWL = 0
                    print(f"Loaded Low MWL PPG: {filename}, Features: {len(features)}")
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    return np.array(X), np.array(y)


def evaluate_random_forest(X, y):
    """
    Train and evaluate a Random Forest model on the PPG dataset.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        random_state=42,
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        bootstrap=True
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)
    mean_cv_score = cv_scores.mean()
    std_cv_score = cv_scores.std()

    print("\n" + "=" * 60)
    print("RANDOM FOREST MODEL RESULTS (PPG)")
    print("=" * 60)
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Cross-validation Mean: {mean_cv_score:.4f} (+/- {std_cv_score * 2:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low MWL', 'High MWL']))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, accuracy, mean_cv_score


def predict_random_samples(model, X, y, accuracy, n=5, show_all_features=False):
    """
    Display random sample predictions with corresponding feature values.
    """
    print("\n" + "=" * 60)
    print(f"PREDICTIONS ON {n} RANDOM SAMPLES (with feature values)")
    print("=" * 60)

    indices = np.random.choice(len(X), size=n, replace=False)
    sample_values = X[indices]
    sample_labels = y[indices]

    for i, (sample, true_label) in enumerate(zip(sample_values, sample_labels), 1):
        print(f"\nSample {i} (True: {'High MWL' if true_label == 1 else 'Low MWL'})")

        if show_all_features:
            print("  Features:", np.array2string(sample, precision=4, separator=", "))
        else:
            print("  Features (first 10):", np.array2string(sample[:10], precision=4, separator=", "), "...")

        sample_input = sample.reshape(1, -1)
        pred = model.predict(sample_input)[0]
        pred_label = "High MWL" if pred == 1 else "Low MWL"

        print(f"  Prediction: {pred_label}  |  Model Accuracy: {accuracy * 100:.2f}%")


if __name__ == "__main__":
    print("Loading PPG data...")
    X, y = load_and_prepare_data(high_path, low_path)

    if len(X) == 0:
        print("No data loaded. Please check your file paths and data files.")
        print(f"Expected folders: {high_path} and {low_path}")
        print("Expected files: p2h.csv–p25h.csv and p2l.csv–p25l.csv")
    else:
        print(f"\nData loaded successfully!")
        print(f"Total samples: {len(X)}")
        print(f"High MWL samples: {np.sum(y == 1)}")
        print(f"Low MWL samples: {np.sum(y == 0)}")
        print(f"Feature dimension: {X.shape[1]}")

        model, test_acc, cv_acc = evaluate_random_forest(X, y)
        predict_random_samples(model, X, y, test_acc, n=5)

        # ---- Save trained model ----
        joblib.dump(model, "best_ppg_model.pkl")
        print(f"\n✅ Saved Random Forest model")
        print("File saved: best_ppg_model.pkl")
