from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load the models
try:
    regressor_model = joblib.load('models/xgb_regressor_model.joblib')
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    regressor_model = None

# Load and prepare the model
def prepare_model():
    df = pd.read_excel("BlinkIT Grocery Data.xlsx", sheet_name="BlinkIT Grocery Data")
    df['Item Weight'] = df['Item Weight'].fillna(df['Item Weight'].mean())
    
    # Prepare encoders
    encoders = {}
    for column in ['Item Type', 'Outlet Size', 'Outlet Location Type', 'Outlet Type']:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        encoders[column] = le
    
    return encoders

# Initialize model and encoders
# Only prepare encoders from the data, as the model is pre-loaded
encoders = prepare_model()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Prepare input data
        input_data = {
            'Item Weight': float(data['item_weight']),
            'Item Visibility': float(data['item_visibility']),
            'Item Type': encoders['Item Type'].transform([data['item_type']])[0],
            'Outlet Size': encoders['Outlet Size'].transform([data['outlet_size']])[0],
            'Outlet Location Type': encoders['Outlet Location Type'].transform([data['outlet_location_type']])[0],
            'Outlet Type': encoders['Outlet Type'].transform([data['outlet_type']])[0],
            'Rating': float(data['rating'])
        }
        
        # Create input DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = regressor_model.predict(input_df)[0]
        
        return jsonify({
            'success': True,
            'predicted_sales': round(float(prediction), 2)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)