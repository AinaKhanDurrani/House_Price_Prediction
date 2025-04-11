from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Load the trained model and column structure
model = pickle.load(open("./House_Price_Prediction_Model.pickle", "rb"))
X_columns = pickle.load(open("./X_columns.pickle", "rb"))

app = Flask(__name__)

# Simple test route
@app.route('/hello', methods=['GET'])
def hello():
    return "Hi from Flask!"

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.get_json()
        return predict(data)
    except Exception as e:
        return jsonify({'error': str(e)})

# Core prediction logic
def predict(data, test=False):
    try:
        Area = data['Area']
        Bedrooms = data['Bedrooms']
        Bathrooms = data['Bathrooms']
        Floors = data['Floors']
        YearBuilt = data['YearBuilt']
        Location = data['Location']
        Condition = data['Condition']
        Garage = data['Garage']

        # Calculate Decade
        Decade = (YearBuilt // 10) * 10

        # Initialize input DataFrame with default values
        input_data = pd.DataFrame({
            'Area': [Area],
            'Bedrooms': [Bedrooms],
            'Bathrooms': [Bathrooms],
            'Floors': [Floors],
            'YearBuilt': [YearBuilt],
            'Decade': [Decade],
            'Location_Downtown': [0],
            'Location_Rural': [0],
            'Location_Suburban': [0],
            'Location_Urban': [0],
            'Condition_Excellent': [0],
            'Condition_Fair': [0],
            'Condition_Good': [0],
            'Condition_Poor': [0],
            'Garage_No': [0],
            'Garage_Yes': [0]
        })

        # Set one-hot encoded values
        input_data[f'Location_{Location}'] = 1
        input_data[f'Condition_{Condition}'] = 1
        input_data[f'Garage_{Garage}'] = 1

        # Reorder columns to match training set
        input_data = input_data[X_columns]

        # Make prediction
        predicted_price = model.predict(input_data)[0]

        if test:
            return {'predicted_price': round(predicted_price, 2)}
        else:
            return jsonify({'predicted_price': round(predicted_price, 2)})

    except Exception as e:
        if test:
            return {'error': str(e)}
        else:
            return jsonify({'error': str(e)})


# Run server or test manually
if __name__ == "__main__":
    test_mode = True  # Change to False to run Flask server

    if test_mode:
        # Manual testing
        test_data = {
            "Area": 2400,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Floors": 2,
            "YearBuilt": 2008,
            "Location": "Urban",
            "Condition": "Good",
            "Garage": "Yes"
        }
        result = predict(test_data, test=True)
        print("Test Prediction Output:", result)
    else:
        print("Starting Python Flask Server For House Price Prediction...")
        app.run(debug=True)
