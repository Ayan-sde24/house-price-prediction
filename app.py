from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model & artifacts once at startup
utils.load_saved_artifacts()


# Root route (FIXES your error)
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Backend is running successfully",
        "endpoints": {
            "GET /get_locations": "Get all available locations",
            "POST /predict": "Predict house price"
        }
    })


# Get all locations
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
            'price': round(estimated_price, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Run server
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    app.run(host="0.0.0.0", port=10000)