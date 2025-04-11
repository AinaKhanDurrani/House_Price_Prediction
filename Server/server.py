from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Load the trained model and feature columns
try:
    model = pickle.load(open("../Model/House_Price_Prediction_Model.pickle", "rb"))
    X_columns = pickle.load(open("X_columns.pickle", "rb"))  # Should match the training columns exactly
except Exception as e:
    raise Exception(f"Model loading failed: {e}")

app = Flask(__name__)

# Test route
@app.route('/hello', methods=['GET'])
def hello():
    return "Hi from Flask!"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)  # Ensures JSON even if header is incorrect

        # Validate required keys
        required_keys = ['Area', 'Bedrooms', 'Bathrooms', 'Floors', 'YearBuilt', 'Location', 'Condition', 'Garage']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({'error': f'Missing keys in request: {missing_keys}'}), 400

        # Extract values
        Area = data['Area']
        Bedrooms = data['Bedrooms']
        Bathrooms = data['Bathrooms']
        Floors = data['Floors']
        YearBuilt = data['YearBuilt']
        Location = data['Location']
        Condition = data['Condition']
        Garage = data['Garage']

        # Create the input DataFrame with all expected one-hot columns
        input_data = pd.DataFrame(columns=X_columns)
        input_data.loc[0] = [0] * len(X_columns)  # Initialize with zeros

        # Set base numeric features
        input_data.at[0, 'Area'] = Area
        input_data.at[0, 'Bedrooms'] = Bedrooms
        input_data.at[0, 'Bathrooms'] = Bathrooms
        input_data.at[0, 'Floors'] = Floors
        input_data.at[0, 'YearBuilt'] = YearBuilt

        # One-hot encoded values - only if the column exists
        loc_col = f'Location_{Location}'
        cond_col = f'Condition_{Condition}'
        garage_col = f'Garage_{Garage}'

        for col in [loc_col, cond_col, garage_col]:
            if col in input_data.columns:
                input_data.at[0, col] = 1
            else:
                print(f"Warning: Column '{col}' not found in model input columns.")

        # Predict the price
        predicted_price = model.predict(input_data)[0]

        return jsonify({'predicted_price': round(predicted_price, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server for House Price Prediction...")
    app.run(debug=True)
