"""
Plant Disease Detector & Pesticide Recommender — SIH25015
-------------------------------------------------------------
- Plant name is OPTIONAL (user can skip it)
- User captures (phone camera) or uploads a leaf photo
- AI detects the disease + confidence + severity
- App recommends pesticide name + amount + treatment steps
- No hardware, no Raspberry Pi, no automatic spraying
- Runs on your PC, monitored from your phone's browser over local Wi-Fi

Run:  python3 main.py   ->  http://localhost:5000  (on PC)
From phone (same Wi-Fi):  http://<your-pc-ip>:5000
"""

# import os
# import time
# import threading
# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# status = {
#     "state": "idle",       # idle | detecting | done | error
#     "plant": None,
#     "disease": None,
#     "confidence": None,
#     "severity": None,
#     "pesticide": None,
#     "dosage_ml": 0,
#     "steps": [],
#     "message": "Waiting for a photo."
# }
# status_lock = threading.Lock()

# history = []
# MAX_HISTORY = 10


# def update_status(**kwargs):
#     with status_lock:
#         status.update(kwargs)


# # --------------------------------------------------------------------------
# # Disease detection (AI) — plug your real trained model in here
# # --------------------------------------------------------------------------
# def detect_disease(image_path: str, plant_type: str):
#     """
#     Replace this with real inference once you have a trained model, e.g.:

#         import numpy as np
#         from PIL import Image
#         import tflite_runtime.interpreter as tflite

#         interpreter = tflite.Interpreter(model_path="model.tflite")
#         interpreter.allocate_tensors()
#         input_details = interpreter.get_input_details()
#         output_details = interpreter.get_output_details()

#         img = Image.open(image_path).resize((224, 224))
#         arr = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
#         interpreter.set_tensor(input_details[0]['index'], arr)
#         interpreter.invoke()
#         prediction = interpreter.get_tensor(output_details[0]['index'])

#         class_names = ["Healthy", "Leaf Blight", "Powdery Mildew", "Rust"]
#         idx = int(prediction.argmax())
#         confidence = float(prediction[0][idx]) * 100
#         return class_names[idx], round(confidence, 1)

#     Note: plant_type may be None/empty since it's optional — a real model
#     trained across multiple crops should still work without it, though
#     accuracy may improve if you route to a per-crop model when it's given.

#     Must return: (disease_name: str, confidence_percent: float)
#     """
#     time.sleep(1.5)  # simulate inference time
#     import random
#     demo_diseases = ["Healthy", "Leaf Blight", "Powdery Mildew", "Rust"]
#     disease = random.choice(demo_diseases)
#     confidence = round(random.uniform(78, 97), 1)
#     return disease, confidence


# def get_severity(confidence: float, disease: str) -> str:
#     """Simple severity heuristic — refine once real model gives per-pixel
#     infected-area data instead of just a class label."""
#     if disease == "Healthy":
#         return "None"
#     if confidence >= 90:
#         return "Severe"
#     if confidence >= 82:
#         return "Moderate"
#     return "Mild"


# # --------------------------------------------------------------------------
# # Pesticide + dosage + treatment steps
# # --------------------------------------------------------------------------
# TREATMENT_TABLE = {
#     "Healthy": {
#         "pesticide": "None needed",
#         "base_dosage_ml": 0,
#         "steps": ["No treatment required.", "Recheck in 5-7 days as routine monitoring."]
#     },
#     "Leaf Blight": {
#         "pesticide": "Mancozeb 75% WP",
#         "base_dosage_ml": 15,
#         "steps": [
#             "Mix recommended dosage in 1 litre of water.",
#             "Spray evenly on both sides of affected leaves.",
#             "Repeat every 7-10 days until symptoms subside.",
#             "Avoid spraying right before rain for best absorption."
#         ]
#     },
#     "Powdery Mildew": {
#         "pesticide": "Sulfur Spray (Wettable Sulfur)",
#         "base_dosage_ml": 10,
#         "steps": [
#             "Mix dosage in 1 litre of water.",
#             "Spray in early morning or evening (avoid midday heat).",
#             "Ensure good air circulation around plants after spraying.",
#             "Repeat weekly until new growth appears healthy."
#         ]
#     },
#     "Rust": {
#         "pesticide": "Propiconazole 25% EC",
#         "base_dosage_ml": 12,
#         "steps": [
#             "Mix dosage in 1 litre of water.",
#             "Remove and discard severely infected leaves before spraying.",
#             "Spray thoroughly, focusing on the underside of leaves.",
#             "Repeat after 14 days if symptoms persist."
#         ]
#     },
# }

# SEVERITY_MULTIPLIER = {"None": 0, "Mild": 0.7, "Moderate": 1.0, "Severe": 1.4}


# def get_treatment_info(disease: str, severity: str):
#     info = TREATMENT_TABLE.get(disease, {
#         "pesticide": "Unknown", "base_dosage_ml": 0, "steps": ["Consult a local agriculture expert."]
#     })
#     multiplier = SEVERITY_MULTIPLIER.get(severity, 1.0)
#     dosage = round(info["base_dosage_ml"] * multiplier, 1)
#     return info["pesticide"], dosage, info["steps"]


# # --------------------------------------------------------------------------
# # Pipeline
# # --------------------------------------------------------------------------
# def run_pipeline(image_path: str, plant_type: str):
#     try:
#         display_plant = plant_type if plant_type else "Not specified"

#         update_status(state="detecting", plant=display_plant, disease=None,
#                       confidence=None, severity=None, pesticide=None,
#                       dosage_ml=0, steps=[], message="Analyzing image...")

#         disease, confidence = detect_disease(image_path, plant_type)
#         severity = get_severity(confidence, disease)
#         pesticide, dosage, steps = get_treatment_info(disease, severity)

#         if dosage > 0:
#             message = f"{disease} detected ({severity} severity, {confidence}% confidence)."
#         else:
#             message = f"Plant looks healthy ({confidence}% confidence)."

#         update_status(state="done", disease=disease, confidence=confidence,
#                       severity=severity, pesticide=pesticide, dosage_ml=dosage,
#                       steps=steps, message=message)

#         with status_lock:
#             history.insert(0, {
#                 "plant": display_plant,
#                 "disease": disease,
#                 "severity": severity,
#                 "confidence": confidence,
#                 "pesticide": pesticide,
#                 "dosage_ml": dosage,
#                 "time": time.strftime("%H:%M:%S")
#             })
#             del history[MAX_HISTORY:]

#     except Exception as e:
#         update_status(state="error", message=f"Error: {e}")


# # --------------------------------------------------------------------------
# # Routes
# # --------------------------------------------------------------------------
# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/analyze", methods=["POST"])
# def analyze():
#     # Plant type is OPTIONAL — may arrive empty or missing entirely
#     plant_type = request.form.get("plant_type", "").strip()
#     image_file = request.files.get("image")

#     if not image_file:
#         return jsonify({"error": "No image received"}), 400

#     filename = f"{int(time.time())}_{image_file.filename}"
#     image_path = os.path.join(UPLOAD_FOLDER, filename)
#     image_file.save(image_path)

#     thread = threading.Thread(target=run_pipeline, args=(image_path, plant_type))
#     thread.start()

#     return jsonify({"message": "Image received. Analyzing..."})


# @app.route("/status")
# def get_status():
#     with status_lock:
#         return jsonify(status)


# @app.route("/history")
# def get_history():
#     with status_lock:
#         return jsonify(history)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)


"""
Plant Disease Detector & Pesticide Recommender — SIH25015
-------------------------------------------------------------
- Plant name is OPTIONAL (user can skip it)
- User captures (phone camera) or uploads a leaf photo
- AI detects the disease + confidence + severity
- App recommends pesticide name + amount + treatment steps
- No hardware, no Raspberry Pi, no automatic spraying
- Runs on your PC, monitored from your phone's browser over local Wi-Fi

Run:  python3 main.py   ->  http://localhost:5000  (on PC)
From phone (same Wi-Fi):  http://<your-pc-ip>:5000
"""

import os
import time
import threading
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

status = {
    "state": "idle",       # idle | detecting | done | error
    "plant": None,
    "disease": None,
    "confidence": None,
    "severity": None,
    "pesticide": None,
    "dosage_ml": 0,
    "steps": [],
    "message": "Waiting for a photo."
}
status_lock = threading.Lock()

history = []
MAX_HISTORY = 10


def update_status(**kwargs):
    with status_lock:
        status.update(kwargs)


# --------------------------------------------------------------------------
# Disease detection
# --------------------------------------------------------------------------
# IMPORTANT: This is a COLOR-BASED HEURISTIC, not a trained neural network.
# It genuinely analyzes the uploaded photo's pixels (unlike the earlier
# placeholder, which returned a random result regardless of the image) —
# but it works by measuring green vs. brown/yellow/white pixel proportions,
# not by learning patterns from thousands of labeled examples. That means:
#   - It WILL correctly flag leaves with visible brown spots, yellowing,
#     or white powdery patches as diseased.
#   - It CAN be fooled by things a real trained model wouldn't be: unusual
#     lighting, autumn-colored but healthy leaves, soil/background color
#     in the shot, or diseases with no strong color signature.
# For real accuracy, replace this with a CNN trained on a labeled dataset
# (e.g. PlantVillage) exported to TensorFlow Lite — a template for that
# swap is included at the bottom of this function.
def analyze_leaf_colors(image_path: str, sample_size=200):
    """Opens the actual image and measures healthy vs unhealthy color regions."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((sample_size, sample_size))
    arr = np.array(img).astype(np.float32) / 255.0

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Healthy green: green channel clearly dominant over red and blue
    green_mask = (g > r * 1.05) & (g > b * 1.05) & (g > 0.25)

    # Yellowing (common in Powdery Mildew / early stress): high R+G, low B
    yellow_mask = (r > 0.5) & (g > 0.5) & (b < 0.45) & (~green_mask)

    # Brown/necrotic spots (common in Blight/Rust): red-dominant, darker
    brown_mask = (r > g) & (r > 0.25) & (r < 0.75) & (b < r * 0.8) & (~green_mask) & (~yellow_mask)

    # White/grayish powdery patches
    white_mask = (r > 0.75) & (g > 0.75) & (b > 0.65) & (np.abs(r - g) < 0.08)

    total = arr.shape[0] * arr.shape[1]
    return {
        "green_pct": round(float(green_mask.sum()) / total * 100, 1),
        "yellow_pct": round(float(yellow_mask.sum()) / total * 100, 1),
        "brown_pct": round(float(brown_mask.sum()) / total * 100, 1),
        "white_pct": round(float(white_mask.sum()) / total * 100, 1),
    }


def detect_disease(image_path: str, plant_type: str):
    """
    Analyzes the actual uploaded image (see analyze_leaf_colors above) and
    classifies it based on which unhealthy color signal is strongest.

    To upgrade to a real trained model later, replace the body of this
    function with something like:

        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path="model.tflite")
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        img = Image.open(image_path).resize((224, 224))
        arr = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
        interpreter.set_tensor(input_details[0]['index'], arr)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        class_names = ["Healthy", "Leaf Blight", "Powdery Mildew", "Rust"]
        idx = int(prediction.argmax())
        confidence = float(prediction[0][idx]) * 100
        return class_names[idx], round(confidence, 1)

    Must return: (disease_name: str, confidence_percent: float)
    """
    time.sleep(1.0)  # brief pause so the "Analyzing..." state is visible in the UI

    stats = analyze_leaf_colors(image_path)
    brown, yellow, white = stats["brown_pct"], stats["yellow_pct"], stats["white_pct"]
    unhealthy_pct = brown + yellow + white

    if unhealthy_pct < 4:
        # Very little discoloration detected -> classify as healthy
        confidence = round(min(92 + unhealthy_pct, 98), 1)
        return "Healthy", confidence

    # Whichever unhealthy signal is strongest decides the disease label
    if white >= brown and white >= yellow:
        disease = "Powdery Mildew"
        strength = white
    elif brown >= yellow:
        disease = "Leaf Blight" if brown > 10 else "Rust"
        strength = brown
    else:
        disease = "Powdery Mildew" if yellow > 15 else "Rust"
        strength = yellow

    confidence = round(min(78 + strength * 1.3, 98), 1)
    return disease, confidence


def get_severity(confidence: float, disease: str) -> str:
    """Simple severity heuristic — refine once real model gives per-pixel
    infected-area data instead of just a class label."""
    if disease == "Healthy":
        return "None"
    if confidence >= 90:
        return "Severe"
    if confidence >= 82:
        return "Moderate"
    return "Mild"


# --------------------------------------------------------------------------
# Pesticide + dosage + treatment steps
# --------------------------------------------------------------------------
TREATMENT_TABLE = {
    "Healthy": {
        "pesticide": "None needed",
        "base_dosage_ml": 0,
        "steps": ["No treatment required.", "Recheck in 5-7 days as routine monitoring."]
    },
    "Leaf Blight": {
        "pesticide": "Mancozeb 75% WP",
        "base_dosage_ml": 15,
        "steps": [
            "Mix recommended dosage in 1 litre of water.",
            "Spray evenly on both sides of affected leaves.",
            "Repeat every 7-10 days until symptoms subside.",
            "Avoid spraying right before rain for best absorption."
        ]
    },
    "Powdery Mildew": {
        "pesticide": "Sulfur Spray (Wettable Sulfur)",
        "base_dosage_ml": 10,
        "steps": [
            "Mix dosage in 1 litre of water.",
            "Spray in early morning or evening (avoid midday heat).",
            "Ensure good air circulation around plants after spraying.",
            "Repeat weekly until new growth appears healthy."
        ]
    },
    "Rust": {
        "pesticide": "Propiconazole 25% EC",
        "base_dosage_ml": 12,
        "steps": [
            "Mix dosage in 1 litre of water.",
            "Remove and discard severely infected leaves before spraying.",
            "Spray thoroughly, focusing on the underside of leaves.",
            "Repeat after 14 days if symptoms persist."
        ]
    },
}

SEVERITY_MULTIPLIER = {"None": 0, "Mild": 0.7, "Moderate": 1.0, "Severe": 1.4}


def get_treatment_info(disease: str, severity: str):
    info = TREATMENT_TABLE.get(disease, {
        "pesticide": "Unknown", "base_dosage_ml": 0, "steps": ["Consult a local agriculture expert."]
    })
    multiplier = SEVERITY_MULTIPLIER.get(severity, 1.0)
    dosage = round(info["base_dosage_ml"] * multiplier, 1)
    return info["pesticide"], dosage, info["steps"]


# --------------------------------------------------------------------------
# Combined diagnosis: ONE function that returns disease + pesticide + amount
# together. This is what run_pipeline() calls, so there's a single, obvious
# place to look if any of these four values ever seem wrong or missing.
# --------------------------------------------------------------------------
def diagnose_and_recommend(image_path: str, plant_type: str) -> dict:
    disease, confidence = detect_disease(image_path, plant_type)
    severity = get_severity(confidence, disease)
    pesticide, dosage_ml, steps = get_treatment_info(disease, severity)

    return {
        "disease": disease,
        "confidence": confidence,
        "severity": severity,
        "pesticide": pesticide,      # <-- name of pesticide to cure the disease
        "dosage_ml": dosage_ml,      # <-- amount (in ml) needed to cure it
        "steps": steps,
    }


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------
def run_pipeline(image_path: str, plant_type: str):
    try:
        display_plant = plant_type if plant_type else "Not specified"

        update_status(state="detecting", plant=display_plant, disease=None,
                      confidence=None, severity=None, pesticide=None,
                      dosage_ml=0, steps=[], message="Analyzing image...")

        result = diagnose_and_recommend(image_path, plant_type)
        disease = result["disease"]
        confidence = result["confidence"]
        severity = result["severity"]
        pesticide = result["pesticide"]      # name of pesticide to cure the disease
        dosage = result["dosage_ml"]          # amount (ml) needed to cure it
        steps = result["steps"]

        if dosage > 0:
            message = f"{disease} detected ({severity} severity, {confidence}% confidence). Use {pesticide} — {dosage} ml."
        else:
            message = f"Plant looks healthy ({confidence}% confidence)."

        update_status(state="done", disease=disease, confidence=confidence,
                      severity=severity, pesticide=pesticide, dosage_ml=dosage,
                      steps=steps, message=message)

        with status_lock:
            history.insert(0, {
                "plant": display_plant,
                "disease": disease,
                "severity": severity,
                "confidence": confidence,
                "pesticide": pesticide,
                "dosage_ml": dosage,
                "time": time.strftime("%H:%M:%S")
            })
            del history[MAX_HISTORY:]

    except Exception as e:
        update_status(state="error", message=f"Error: {e}")


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # Plant type is OPTIONAL — may arrive empty or missing entirely
    plant_type = request.form.get("plant_type", "").strip()
    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "No image received"}), 400

    filename = f"{int(time.time())}_{image_file.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    thread = threading.Thread(target=run_pipeline, args=(image_path, plant_type))
    thread.start()

    return jsonify({"message": "Image received. Analyzing..."})


@app.route("/status")
def get_status():
    with status_lock:
        return jsonify(status)


@app.route("/history")
def get_history():
    with status_lock:
        return jsonify(history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)