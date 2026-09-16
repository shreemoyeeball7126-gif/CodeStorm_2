Historical Data
      ↓
Demand Prediction
      ↓
Meal Preparation Analysis
      ↓
Surplus Detection
      ↓
Food-Safety Verification
      ↓
Surplus Redistribution
      ↓
Environmental & Financial Impact

The system helps answer:
"How much food should we prepare, how much surplus do we have, and what impact can we avoid?" 

✨ Key Features
📊 Demand Prediction
Uses a trained machine-learning model to estimate meal demand based on factors such as:
Attendance
Day of the week
Weather conditions
Historical food-service patterns
🥘 Surplus Detection
Compares:
Food Prepared − Predicted Demand
to determine the number of surplus meals.
Negative surplus is automatically prevented from being treated as waste.
🛡️ Food-Safety Verification
The prototype includes checks for:
Storage duration
Storage temperature
Only food that satisfies the configured safety conditions proceeds through the redistribution logic.
⚠️ The current safety thresholds are prototype values and should be verified against applicable food-safety regulations before real-world deployment.
🤝 Surplus Matching
Safe surplus can be allocated to predefined recipients according to:
Priority
Distance
Recipient capacity
🌱 Impact Estimation
FoodWise estimates:
Food saved
Money saved
Carbon emissions avoided
📈 Historical Data Visualization
The dashboard provides a visualization of food preparation and meals served across the available 250-day dataset.

🧠 Machine Learning Pipeline
The demand prediction component uses historical food-service data.
The model receives:
Attendance
Day of Week
Weather
and predicts:
Predicted Meal Demand
Categorical variables are encoded before being passed to the trained model.
The trained model is stored as:
demand_model.pkl

🖥️ Dashboard
FoodWise includes a Streamlit dashboard that provides:
📅 Date selection
⏱️ Storage-time input
🌡️ Storage-temperature input
📊 Demand prediction
🥘 Surplus calculation
🌱 Environmental impact
💰 Financial impact
📈 Historical data visualization

Dashboard Flow
Select Date
     ↓
Run FoodWise Analysis
     ↓
Demand Overview
     ↓
Surplus Detection
     ↓
Impact Estimation

📁 Project Structure
SIH_S38/
│
├── app.py                  # Streamlit dashboard
├── pipeline.py             # Main FoodWise pipeline
├── predict.py              # ML demand prediction
├── surplus_logic.py        # Surplus & redistribution logic
├── impact.py               # Environmental & financial impact
│
├── demand_model.pkl        # Trained ML model
├── demand_data.csv         # Demand-model dataset
├── food_waste_250_days.csv # 250-day food-service dataset
│
├── make_data.py            # Dataset generation
├── generate_data.py        # Data generation utilities
├── explore_data.py         # Data exploration
├── train_model.py          # Model training
│
├── integration_test.py     # Integration testing
├── test_pipeline.py       # Pipeline tests
├── test_surplus.py        # Surplus logic tests
│
├── code.py                # Dashboard-related code
├── style.css              # Dashboard styling
└── README.md              # Project documentation

🔄 System Architecture
                 ┌─────────────────────┐
                 │   Historical Data   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   ML Prediction     │
                 │   Demand Forecast   │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │   Surplus Calculation    │
              │ Prepared - Predicted     │
              └────────────┬─────────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │   Safety Check      │
                 │ Time + Temperature  │
                 └──────────┬──────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                   Safe          Unsafe
                     │             │
                     ▼             ▼
             ┌──────────────┐   ┌───────────┐
             │ Redistribution│   │ Unmatched │
             └───────┬──────┘   │  Surplus  │
                     │           └───────────┘
                     ▼
             ┌─────────────────┐
             │ Impact Analysis │
             └─────────────────┘
🧪 Testing
The FoodWise pipeline has been tested across:
✅ 250-day dataset loading
✅ First-date data retrieval
✅ Last-date data retrieval
✅ Surplus calculation
✅ Negative surplus protection
✅ Meal-to-kg conversion
✅ Environmental impact calculation
✅ Complete pipeline integration
✅ Output validation
Current test result:
================================
       FOODWISE TESTING
================================

✅ 250-day dataset test PASSED
✅ First date test PASSED
✅ Last date test PASSED
✅ Surplus calculation PASSED
✅ Negative surplus protection PASSED
✅ KG conversion PASSED
✅ Impact calculation PASSED
✅ Complete pipeline PASSED
✅ Output validation PASSED

🎉 ALL TESTS PASSED!

⚙️ Installation
1. Clone the repository
git clone https://github.com/shreemoyeeball7126-gif/CodeStorm.git
cd CodeStorm
2. Install dependencies
pip install pandas streamlit scikit-learn
3. Run the dashboard
streamlit run app.py
The dashboard will open in your browser.

🧪 Run Tests
To test the complete pipeline:
python test_pipeline.py
To test surplus logic:
python test_surplus.py

📌 Current Prototype Scope
FoodWise is currently a working prototype demonstrating the core demand forecasting, surplus detection, safety-check, redistribution logic, and impact-estimation workflow.
The current system uses a prepared historical dataset and predefined redistribution recipients.
For production deployment, the system could be extended with:
Real-time attendance integration
Live weather APIs
Real institutional kitchen data
Database-backed recipient management
Real-time notifications
Verified food-safety standards
Authentication and role-based access
Cloud deployment
Automated redistribution coordination

🌍 Expected Impact
FoodWise aims to help institutions move from:
"Prepare more just in case."
to:
"Prepare based on predicted demand."
By reducing unnecessary preparation and identifying usable surplus, institutions can potentially reduce:
🍚 Food waste
💰 Operational costs
🌱 Environmental impact
while improving the efficiency of campus food management.

👥 Team
Team CodeStorm
Built for:
🇮🇳 Smart India Hackathon 2026
Problem Area: Food-Service Demand Forecasting & Surplus Redistribution
❤️ Built with
Python · Pandas · Scikit-learn · Streamlit · Machine Learning
🍽️ FoodWise
Smarter demand. Less waste. Greater impact. 🌱
