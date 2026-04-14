from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/get_locations', methods=['GET'])
def get_locations():
    locations = utils.get_location_names()
    return jsonify({
        'locations': [loc.title() for loc in locations]
    })

@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        data = request.get_json()
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])
        
        estimated_price = utils.get_estimated_price(location, total_sqft, bhk, bath)
        
        return jsonify({
            'price': estimated_price
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    utils.load_saved_artifacts()
    app.run(host="0.0.0.0", port=10000)
