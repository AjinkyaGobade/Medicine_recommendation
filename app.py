from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests
from datetime import datetime
from extensions import db, login_manager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicine_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)

# Import models and routes after initializing db to avoid circular imports
from models import User, Symptom, Disease, Medicine, PatientHistory
from routes import register_routes

# Register routes
register_routes(app)

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)