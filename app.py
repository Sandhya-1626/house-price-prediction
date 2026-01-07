import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the trained model
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    model = None
    print("Error: model.pkl not found. Please run model_train.py first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    
    try:
        # Extract features from JSON
        area = float(data['area'])
        bedrooms = int(data['bedrooms'])
        bathrooms = int(data['bathrooms'])
        
        # Prepare feature vector (must match model's training input: area, bedrooms, bathrooms)
        features = np.array([[area, bedrooms, bathrooms]])
        
        # Predict
        prediction = model.predict(features)
        
        # Format output
        output = round(prediction[0], 2)
        
        return jsonify({'price': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
