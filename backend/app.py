import os
import traceback
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "models", "churn_model.pkl"))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# ---------- Load model (pipeline) ----------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

print("Loading model from:", MODEL_PATH)
model = joblib.load(MODEL_PATH)
print("Model loaded. Type:", type(model))

# ---------- Flask app (serve static files from frontend) ----------
app = Flask(__name__, template_folder=FRONTEND_DIR, static_folder=FRONTEND_DIR)


# Utility: try to extract expected raw input column names from the saved pipeline's preprocessor
def get_expected_input_columns(saved_model):
    """
    Try to discover the raw input column names used at training time by inspecting
    the pipeline inside the saved model. Returns a list or None if not found.
    """
    base = None
    # If wrapped in CalibratedClassifierCV, try common attributes:
    if hasattr(saved_model, "base_estimator_"):
        base = saved_model.base_estimator_
    elif hasattr(saved_model, "estimator_"):
        base = saved_model.estimator_
    elif hasattr(saved_model, "estimator"):
        base = saved_model.estimator
    else:
        base = saved_model  # maybe it's already a pipeline

    # base should be a Pipeline or ImbPipeline with a preprocessing step named 'prep' or similar
    preproc = None
    if hasattr(base, "named_steps"):
        # Common names: 'prep', 'preprocessor', 'preprocessing', 'prep'
        for candidate in ("prep", "preprocessor", "preprocessing", "preprocess"):
            if candidate in base.named_steps:
                preproc = base.named_steps[candidate]
                break
        # fallback: if there's a step that is a ColumnTransformer, pick it
        if preproc is None:
            for name, step in base.named_steps.items():
                # identify ColumnTransformer by attribute 'transformers_'
                if hasattr(step, "transformers_"):
                    preproc = step
                    break

    if preproc is None:
        return None

    # preproc should be a ColumnTransformer; its .transformers_ contains (name, transformer, columns)
    cols = []
    try:
        for name, transformer, col_names in preproc.transformers_:
            # col_names sometimes is "remainder" or slice — skip those
            if isinstance(col_names, (list, tuple, np.ndarray)):
                cols.extend(list(col_names))
    except Exception:
        # fallback: try to use get_feature_names_out if present (but that is after fit, and returns expanded)
        try:
            cols = list(preproc.feature_names_in_)
        except Exception:
            cols = []

    return cols if cols else None


EXPECTED_COLS = get_expected_input_columns(model)
print("Discovered expected input columns:", EXPECTED_COLS)

# cols that had 'No internet service' in training; normalize them if user sends that string
NO_SERVICE_COLS = [
    'MultipleLines','OnlineSecurity','OnlineBackup',
    'DeviceProtection','TechSupport','StreamingTV','StreamingMovies'
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        print("Incoming JSON:", data)

        if not isinstance(data, dict):
            return jsonify({"error": "Request JSON must be an object with feature keys"}), 400

        # Build DataFrame from incoming JSON
        input_df = pd.DataFrame([data])

        # Normalize known "No internet/phone service" tokens to "No"
        for c in NO_SERVICE_COLS:
            if c in input_df.columns:
                input_df[c] = input_df[c].replace({'No internet service': 'No', 'No phone service': 'No'})

        # Ensure expected columns exist
        if EXPECTED_COLS is not None:
            missing = [c for c in EXPECTED_COLS if c not in input_df.columns]
            for c in missing:
                input_df[c] = np.nan
            input_df = input_df.reindex(columns=EXPECTED_COLS)

        # Coerce numeric-looking strings
        for col in input_df.columns:
            if input_df[col].dtype == object:
                converted = pd.to_numeric(input_df[col], errors='coerce')
                if converted.notnull().any():
                    input_df[col] = converted

        # Predict
        pred = model.predict(input_df)
        proba = model.predict_proba(input_df)[:, 1]

        prediction = int(pred[0])
        probability_percent = float(proba[0]) * 100

        # Discount mapping function
        def get_discount(prob):
            if prob >= 80:
                return 25
            elif prob >= 60:
                return 20
            elif prob >= 40:
                return 15
            elif prob >= 20:
                return 10
            else:
                return 0

        discount = get_discount(probability_percent)

        print(f"PREDICTION: {prediction}, PROB: {probability_percent:.2f}%, DISCOUNT: {discount}%")

        return jsonify({
            "prediction": prediction,
            "probability": round(probability_percent, 2),
            "suggested_discount": discount
        })

    except Exception as exc:
        print("❌ Exception during /predict")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "detail": str(exc)}), 500

if __name__ == "__main__":
    # Run from backend directory. Listen only on localhost by default.
    print("Starting Flask app (debug mode). Frontend folder:", FRONTEND_DIR)
    app.run(host="127.0.0.1", port=5000, debug=True)
    
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))  
#     print(f"Starting Flask app on port {port}. Frontend folder: {FRONTEND_DIR}")
#     app.run(host="0.0.0.0", port=port, debug=False)
