Blinkit Sales Prediction: Big Data-Driven Demand Forecasting
A Big Data & Machine Learning-based project built to forecast grocery item sales for Blinkit, enabling smarter inventory decisions, better marketing, and reduced wastage.

Project Overview
This project demonstrates how Big Data and Machine Learning can be integrated to solve real-world problems in the retail sector. Our solution predicts sales for a given product-outlet combination using historical sales data and advanced analytics techniques. It features a full-stack implementation including data ingestion, distributed processing, predictive modeling, and a responsive web interface.

Features
Cleaned and structured grocery sales dataset
Trained predictive models using XGBoost, CatBoost, and GridSearchCV
Big Data pipeline with MongoDB and PySpark
Flask-based web application for real-time predictions
Sales dashboards using matplotlib, seaborn, and Power BI
User-friendly and responsive frontend

Tech Stack
Data Engineering & Storage
MongoDB (NoSQL)
pandas, numpy for data preprocessing
PySpark for distributed processing
Machine Learning
XGBoost, CatBoost, scikit-learn
GridSearchCV for hyperparameter tuning
joblib for model serialization
Web Development
Flask for backend API
HTML, CSS for frontend
Visualization
matplotlib, seaborn, Power BI

👥 Team Members & Contributions
Name	Role & Contributions
Udit Vedwal	Machine Learning, Model Training & Web Integration
Akshay Khugshal	Data Cleaning, Preprocessing, Database Management, EDA
Vanshika Bhandari	Frontend (HTML/CSS), Power BI Visualization

✅ Testing & Validation
Component	Status	Notes
Model Evaluation	✅ Pass	High accuracy & R² score
Model Persistence	✅ Pass	Serialized using joblib
Web App Functionality	✅ Pass	All routes tested
Prediction Endpoint	✅ Pass	Returns valid results

📈 Results & Insights
Accurate prediction of product-level sales
Real-time inference via a web interface
Visual sales trends, top items, outlet segmentation

📥 How to Run Locally
Clone the repository
git clone https://github.com/uditvedwal-01/Blinkit_Sales_Analysis.git

Install dependencies
pip install -r requirements.txt

Run the Flask app
python app.py

Open your browser at
http://127.0.0.1:5000/

🔗 Live Demo & GitHub Link
GitHub: Blinkit_Sales_Analysis

📄 License
This project is for educational and demonstration purposes only.

