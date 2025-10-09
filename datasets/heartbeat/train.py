#Emotions: SAD, NEUTRAL, ANGRY 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import warnings
import joblib

warnings.filterwarnings('ignore')


def load_heart_rate_data(filepath, sample_size=42985):
    """
    Load and prepare the heart rate dataset.
    Keeps only 'sad', 'neutral', and 'angry' emotions.
    """
    df = pd.read_csv(filepath)

    if 'HeartRate' not in df.columns or 'Emotion' not in df.columns:
        raise ValueError("CSV must contain 'HeartRate' and 'Emotion' columns")

    allowed_emotions = ['neutral', 'sad', 'angry']
    df = df[df['Emotion'].isin(allowed_emotions)].reset_index(drop=True)

    print(f"✅ Filtered dataset to {len(df)} rows with emotions: {allowed_emotions}")

    if sample_size is not None and len(df) > sample_size:
        print(f"Dataset has {len(df)} rows — sampling {sample_size} for faster training.")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    else:
        print(f"Dataset has {len(df)} rows — using all samples.")

    X = df[['HeartRate']].values
    y = df['Emotion'].values

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print("Emotion Classes (encoded):", list(label_encoder.classes_))
    return X, y_encoded, label_encoder


def evaluate_random_forest(X, y, label_encoder):
    """
    Train and evaluate a Random Forest classifier for heart rate emotion classification.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        random_state=42,
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        bootstrap=True
    )

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, scaler.transform(X), y, cv=5)
    mean_cv = cv_scores.mean()
    std_cv = cv_scores.std()

    print("\n" + "=" * 60)
    print("RANDOM FOREST MODEL RESULTS")
    print("=" * 60)
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Cross-validation Mean: {mean_cv:.4f} (+/- {std_cv * 2:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, scaler, accuracy, mean_cv


def predict_random_samples(model, scaler, X, y, label_encoder, accuracy, n=5):
    """
    Show predictions on random samples.
    """
    print("\n" + "=" * 60)
    print(f"PREDICTIONS ON {n} RANDOM SAMPLES")
    print("=" * 60)

    indices = np.random.choice(len(X), size=n, replace=False)
    sample_values = X[indices]
    sample_labels = y[indices]

    for i, (sample, true_label) in enumerate(zip(sample_values, sample_labels), 1):
        true_name = label_encoder.inverse_transform([true_label])[0]
        scaled_sample = scaler.transform(sample.reshape(1, -1))
        pred = model.predict(scaled_sample)[0]
        pred_name = label_encoder.inverse_transform([pred])[0]

        print(f"\nSample {i}:")
        print(f"  Heart Rate: {sample[0]:.2f}")
        print(f"  True Emotion: {true_name}")
        print(f"  Predicted Emotion: {pred_name}")
        print(f"  Model Accuracy: {accuracy * 100:.2f}%")


if __name__ == "__main__":
    filepath = "heart_rate_emotion_dataset.csv"

    print("Loading heart rate dataset...")
    X, y, label_encoder = load_heart_rate_data(filepath)
    print(f"Loaded {len(X)} samples for training.")

    model, scaler, test_acc, cv_acc = evaluate_random_forest(X, y, label_encoder)
    predict_random_samples(model, scaler, X, y, label_encoder, test_acc, n=5)

    # ---- Save trained model and scaler ----
    joblib.dump(model, "best_heartbeat_model.pkl")
    joblib.dump(scaler, "heartbeat_scaler.pkl")
    joblib.dump(label_encoder, "heartbeat_label_encoder.pkl")

    print(f"\n✅ Saved Random Forest model, scaler, and label encoder.")
    print("Files saved:")
    print(" - best_heartbeat_model.pkl")
    print(" - heartbeat_scaler.pkl")
    print(" - heartbeat_label_encoder.pkl")
