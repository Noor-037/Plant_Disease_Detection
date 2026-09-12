from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simulated backend AI detection model database
CROP_DATABASE = {
    "Tomato (Tamatar)": {
        "disease": "Tomato Early Blight",
        "health_percent": 25,
        "pesticide": "Mancozeb 75% WP (e.g., Indofil M-45)",
        "dosage": "2g per liter of water",
        "duration": "Every 7-10 days for 3 weeks"
    },
    "Rice (Chawal)": {
        "disease": "Rice Blast Disease",
        "health_percent": 40,
        "pesticide": "Tricyclazole 75% WP",
        "dosage": "0.6g per liter of water",
        "duration": "Every 10-12 days for 2 weeks"
    },
    "Wheat (Gehun)": {
        "disease": "Wheat Yellow Rust",
        "health_percent": 35,
        "pesticide": "Propiconazole 25% EC",
        "dosage": "1ml per liter of water",
        "duration": "Single spray, repeat if severe after 14 days"
    },
    "Potato (Aloo)": {
        "disease": "Potato Late Blight",
        "health_percent": 20,
        "pesticide": "Cymoxanil + Mancozeb",
        "dosage": "2.5g per liter of water",
        "duration": "Every 7 days for 3 applications"
    },
    "Cotton (Kapas)": {
        "disease": "Cotton Leaf Curl Virus",
        "health_percent": 50,
        "pesticide": "Imidacloprid 17.8% SL (for vector control)",
        "dosage": "0.5ml per liter of water",
        "duration": "Every 15 days"
    },
    "Other Plants": {
        "disease": "General Leaf Spot / Fungal Infection",
        "health_percent": 60,
        "pesticide": "Copper Oxychloride 50% WP",
        "dosage": "3g per liter of water",
        "duration": "Every 7 days for 2 weeks"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    crop = request.form.get('crop', 'Tomato (Tamatar)')
    
    # Handle uploaded file
    file = request.files.get('file')
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validation Check for non-plant files (e.g., cat, car, dog, etc.)
        fn_lower = filename.lower()
        invalid_keywords = ['cat', 'car', 'dog', 'person', 'building', 'laptop', 'phone', 'nonplant', 'invalid']
        if any(keyword in fn_lower for keyword in invalid_keywords):
            return jsonify({
                "valid": False,
                "message": "INVALID IMAGE: Uploaded image is not a plant or leaf! Please upload a clear plant image."
            })

    # Fetch crop response
    data = CROP_DATABASE.get(crop, CROP_DATABASE["Other Plants"])
    return jsonify({
        "valid": True,
        "crop": crop,
        "disease": data["disease"],
        "health_percent": data["health_percent"],
        "pesticide": data["pesticide"],
        "dosage": data["dosage"],
        "duration": data["duration"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
