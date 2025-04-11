from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
from flask_cors import CORS

# Load the model and column structure
model = pickle.load(open("House_Price_Prediction_Model.pickle", "rb"))
X_columns = pickle.load(open("X_columns.pickle", "rb"))

app = Flask(__name__, template_folder='../Client',static_folder='../client/static')  # tells Flask where to find App.html
CORS(app, origins=["*"], supports_credentials=True)  # Be restrictive in prod

@app.route('/')
def index():
    return render_template('App.html')  # Looks in 'Client/App.html'


@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.get_json()
        return make_prediction(data)
    except Exception as e:
        return jsonify({'error': str(e)})

def make_prediction(data):
    try:
        Area = data['Area']
        Bedrooms = data['Bedrooms']
        Bathrooms = data['Bathrooms']
        Floors = data['Floors']
        YearBuilt = data['YearBuilt']
        Location = data['Location']
        Condition = data['Condition']
        Garage = data['Garage']

        Decade = (YearBuilt // 10) * 10

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

        input_data[f'Location_{Location}'] = 1
        input_data[f'Condition_{Condition}'] = 1
        input_data[f'Garage_{Garage}'] = 1

        input_data = input_data[X_columns]

        predicted_price = model.predict(input_data)[0]
        return jsonify({'predicted_price': round(predicted_price, 2)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)