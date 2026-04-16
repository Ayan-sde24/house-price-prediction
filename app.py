from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)

# Load model ONCE at startup
print("Loading model artifacts...")
utils.load_saved_artifacts()
print("Model loaded successfully")


# Root route (fixes "Not Found")
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Backend is running successfully",
        "endpoints": {
            "GET /get_locations": "Get all available locations",
            "POST /predict": "Predict house price"
        }
    })


# Get locations
@app.route('/get_locations', methods=['GET'])
def get_locations():
    try:
        locations = utils.get_location_names()
        return jsonify({
            'locations': [loc.title() for loc in locations]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Predict price
@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        data = request.get_json()

        # Validate input
        required_fields = ['total_sqft', 'location', 'bhk', 'bath']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])

        estimated_price = utils.get_estimated_price(
            location, total_sqft, bhk, bath
        )

        return jsonify({
            'price': estimated_price
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)