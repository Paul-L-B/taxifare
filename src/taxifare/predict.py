from pathlib import Path

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "modelslinreg_pipeline.joblib"
)


def load_model():
    """Load the trained pipeline from disk."""
    return joblib.load(MODEL_PATH)


def predict(model, data):
    """Make predictions using the loaded pipeline."""
    return model.predict(data)


if __name__ == "__main__":
    model = load_model()
    print("Model loaded successfully!")
