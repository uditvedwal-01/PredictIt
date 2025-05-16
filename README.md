# BlinkIT Sales Predictor

A web application that predicts future sales for BlinkIT grocery items based on various features using machine learning.

## Features

- User-friendly web interface
- Real-time sales predictions
- Support for various item types and outlet characteristics
- Responsive design that works on all devices
- Machine learning model trained on historical sales data

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- MongoDB (for data storage)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd blinkit-sales-predictor
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running on your system

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Fill in the form with the following information:
   - Item Weight
   - Item Visibility
   - Item Fat Content
   - Item Type
   - Outlet Size
   - Outlet Location Type
   - Outlet Type
   - Outlet Establishment Year

2. Click the "Predict Sales" button to get the sales prediction

3. The predicted sales value will be displayed in Indian Rupees (₹)

## Data Description

The model uses the following features for prediction:
- Item Weight: Weight of the product
- Item Visibility: The percentage of total display area of all products in store allocated to this particular product
- Item Fat Content: Whether the product is low fat or regular
- Item Type: The category to which the product belongs
- Outlet Size: The size of the store
- Outlet Location Type: The type of area where the store is located
- Outlet Type: Whether the outlet is a grocery store or supermarket
- Outlet Establishment Year: The year in which the store was established

## Contributing

Feel free to submit issues and enhancement requests! 