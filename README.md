# Medicine Recommendation System

A fully functional Medicine Recommendation System built with Python Flask, SQLite, and free APIs. This system allows users to input their symptoms and receive personalized medicine recommendations based on predicted diseases.

## Features

- User registration and login (patient only)
- Symptom input form with age, gender, and allergies
- Disease prediction based on symptoms using a rule-based mapping system
- Medicine recommendations based on predicted disease
- Integration with OpenFDA API for drug information and dosage
- Integration with RxNorm API for drug interactions and warnings
- Allergy and drug interaction warnings
- Clean web interface displaying predicted disease, recommended medicines, dosage, and warnings
- SQLite database for storing patient data and results
- Admin panel for updating disease-medicine mappings

## Project Structure

```
Medicine_recommendation/
├── app.py                  # Main application file
├── models.py               # Database models
├── routes.py               # Application routes and API endpoints
├── seed_data.py            # Script to populate database with initial data
├── requirements.txt        # Python dependencies
├── static/                 # Static files
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   └── js/
│       └── script.js      # Custom JavaScript
└── templates/              # HTML templates
    ├── admin.html          # Admin panel
    ├── base.html           # Base template with layout
    ├── dashboard.html      # User dashboard
    ├── index.html          # Home page
    ├── login.html          # Login page
    ├── register.html       # Registration page
    ├── results.html        # Results page showing recommendations
    └── symptoms.html       # Symptom input form
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository to your local machine

2. Navigate to the project directory:
   ```
   cd Medicine_recommendation
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Initialize the database and seed it with initial data:
   ```
   python seed_data.py
   ```

7. Run the application:
   ```
   python app.py
   ```

8. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Patient User

1. Register a new account or login with existing credentials
2. Navigate to "Check Symptoms" from the dashboard
3. Enter your age, gender, select symptoms, and list any allergies
4. Submit the form to receive disease prediction and medicine recommendations
5. View detailed information about recommended medicines, including dosage and warnings

### Admin User

1. Login with admin credentials (default: username: `admin`, password: `admin123`)
2. Access the admin panel from the navigation menu
3. Add new diseases, symptoms, and medicines
4. Create mappings between diseases and symptoms (with weights)
5. Create mappings between diseases and medicines

## APIs Used

- **OpenFDA API**: Used to fetch drug information, dosage, and side effects
- **RxNorm API**: Used to fetch drug interactions and warnings

## License

This project is open-source and available for personal and educational use.

## Disclaimer

This system is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.