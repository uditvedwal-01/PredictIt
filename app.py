from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Load the models
try:
    classifier_model = joblib.load('models/xgb_classifier_model.joblib')
    regressor_model = joblib.load('models/xgb_regressor_model.joblib')
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    classifier_model = None
    regressor_model = None

# Load and prepare the model
def prepare_model():
    df = pd.read_excel("BlinkIT Grocery Data.xlsx", sheet_name="BlinkIT Grocery Data")
    df['Item Weight'] = df['Item Weight'].fillna(df['Item Weight'].mean())
    df['Outlet Age'] = 2025 - df['Outlet Establishment Year']
    df['Item Fat Content'] = df['Item Fat Content'].replace({'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'})
    
    # Features for prediction
    features = ['Item Weight', 'Item Visibility', 'Item Fat Content', 'Item Type', 
                'Outlet Size', 'Outlet Location Type', 'Outlet Type', 'Outlet Age']
    
    # Prepare encoders
    encoders = {}
    for column in ['Item Fat Content', 'Item Type', 'Outlet Size', 'Outlet Location Type', 'Outlet Type']:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        encoders[column] = le
    
    # Train model
    X = df[features]
    y = df['Sales']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, encoders

# Initialize model and encoders
model, encoders = prepare_model()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you would typically save the contact form data or send an email
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Prepare input data
        input_data = {
            'Item Weight': float(data['item_weight']),
            'Item Visibility': float(data['item_visibility']),
            'Item Fat Content': encoders['Item Fat Content'].transform([data['item_fat_content']])[0],
            'Item Type': encoders['Item Type'].transform([data['item_type']])[0],
            'Outlet Size': encoders['Outlet Size'].transform([data['outlet_size']])[0],
            'Outlet Location Type': encoders['Outlet Location Type'].transform([data['outlet_location_type']])[0],
            'Outlet Type': encoders['Outlet Type'].transform([data['outlet_type']])[0],
            'Outlet Age': 2025 - int(data['outlet_establishment_year'])
        }
        
        # Create input DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'success': True,
            'predicted_sales': round(prediction, 2)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/outlet-analysis')
def outlet_analysis():
    """Render the outlet analysis page"""
    return render_template('outlet_analysis.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)