from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Symptom, Disease, Medicine, PatientHistory, DiseaseSymptom, DiseaseMedicine
from extensions import db, login_manager
import requests
import json
from collections import Counter

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # User registration
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Check if user already exists
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists')
                return redirect(url_for('register'))
            
            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                flash('Email already registered')
                return redirect(url_for('register'))
            
            # Create new user
            new_user = User(username=username, 
                           email=email, 
                           password=generate_password_hash(password, method='sha256'))
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    # User login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('login'))
            
            login_user(user)
            return redirect(url_for('dashboard'))
        
        return render_template('login.html')
    
    # User logout
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # User dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get user's history
        history = PatientHistory.query.filter_by(user_id=current_user.id).order_by(PatientHistory.created_at.desc()).all()
        return render_template('dashboard.html', history=history, Symptom=Symptom)
    
    # Symptom input form
    @app.route('/symptoms', methods=['GET', 'POST'])
    @login_required
    def symptoms():
        if request.method == 'POST':
            age = request.form.get('age')
            gender = request.form.get('gender')
            symptom_ids = request.form.getlist('symptoms')
            allergies = request.form.get('allergies')
            
            # Predict disease based on symptoms
            predicted_disease = predict_disease(symptom_ids)
            
            if predicted_disease:
                # Get recommended medicines
                medicines = get_recommended_medicines(predicted_disease.id, allergies)
                
                # Save patient history
                history = PatientHistory(
                    user_id=current_user.id,
                    age=age,
                    gender=gender,
                    symptoms=','.join(symptom_ids),
                    allergies=allergies,
                    predicted_disease=predicted_disease.id,
                    recommended_medicines=','.join([str(m['id']) for m in medicines]) if medicines else None
                )
                
                db.session.add(history)
                db.session.commit()
                
                return render_template('results.html', 
                                      disease=predicted_disease, 
                                      medicines=medicines, 
                                      age=age, 
                                      gender=gender, 
                                      allergies=allergies)
            else:
                flash('Could not predict disease based on provided symptoms. Please try again.')
                return redirect(url_for('symptoms'))
        
        # Get all symptoms for the form
        symptoms = Symptom.query.all()
        return render_template('symptoms.html', symptoms=symptoms)
    
    # Admin panel
    @app.route('/admin')
    @login_required
    def admin():
        # Simple admin check - in a real app, use proper role-based access control
        if current_user.username != 'admin':
            flash('Admin access required')
            return redirect(url_for('dashboard'))
        
        diseases = Disease.query.all()
        symptoms = Symptom.query.all()
        medicines = Medicine.query.all()
        
        return render_template('admin.html', 
                              diseases=diseases, 
                              symptoms=symptoms, 
                              medicines=medicines)
    
    # API routes for admin panel
    @app.route('/api/disease', methods=['POST'])
    @login_required
    def add_disease():
        if current_user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        disease = Disease(name=data['name'], description=data.get('description', ''))
        db.session.add(disease)
        db.session.commit()
        
        return jsonify({'id': disease.id, 'name': disease.name})
    
    @app.route('/api/symptom', methods=['POST'])
    @login_required
    def add_symptom():
        if current_user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        symptom = Symptom(name=data['name'], description=data.get('description', ''))
        db.session.add(symptom)
        db.session.commit()
        
        return jsonify({'id': symptom.id, 'name': symptom.name})
    
    @app.route('/api/medicine', methods=['POST'])
    @login_required
    def add_medicine():
        if current_user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        medicine = Medicine(
            name=data['name'], 
            description=data.get('description', ''),
            dosage=data.get('dosage', ''),
            side_effects=data.get('side_effects', '')
        )
        db.session.add(medicine)
        db.session.commit()
        
        return jsonify({'id': medicine.id, 'name': medicine.name})
    
    @app.route('/api/disease_symptom', methods=['POST'])
    @login_required
    def add_disease_symptom():
        if current_user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        disease_symptom = DiseaseSymptom(
            disease_id=data['disease_id'],
            symptom_id=data['symptom_id'],
            weight=data.get('weight', 1.0)
        )
        db.session.add(disease_symptom)
        db.session.commit()
        
        return jsonify({'id': disease_symptom.id})
    
    @app.route('/api/disease_medicine', methods=['POST'])
    @login_required
    def add_disease_medicine():
        if current_user.username != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        disease_medicine = DiseaseMedicine(
            disease_id=data['disease_id'],
            medicine_id=data['medicine_id'],
            primary_treatment=data.get('primary_treatment', False)
        )
        db.session.add(disease_medicine)
        db.session.commit()
        
        return jsonify({'id': disease_medicine.id})

# Helper function to predict disease based on symptoms
def predict_disease(symptom_ids):
    # Convert symptom_ids to integers
    symptom_ids = [int(id) for id in symptom_ids]
    
    # Get all diseases and their associated symptoms
    disease_symptoms = DiseaseSymptom.query.filter(DiseaseSymptom.symptom_id.in_(symptom_ids)).all()
    
    if not disease_symptoms:
        return None
    
    # Count occurrences of each disease
    disease_counts = Counter()
    disease_weights = {}
    
    for ds in disease_symptoms:
        disease_counts[ds.disease_id] += 1
        if ds.disease_id not in disease_weights:
            disease_weights[ds.disease_id] = 0
        disease_weights[ds.disease_id] += ds.weight
    
    # Find the disease with the highest count and weight
    max_count = 0
    max_weight = 0
    predicted_disease_id = None
    
    for disease_id, count in disease_counts.items():
        weight = disease_weights[disease_id]
        if count > max_count or (count == max_count and weight > max_weight):
            max_count = count
            max_weight = weight
            predicted_disease_id = disease_id
    
    if predicted_disease_id:
        return Disease.query.get(predicted_disease_id)
    
    return None

# Helper function to get recommended medicines for a disease
def get_recommended_medicines(disease_id, allergies=None):
    # Get medicines for the disease
    disease_medicines = DiseaseMedicine.query.filter_by(disease_id=disease_id).all()
    
    if not disease_medicines:
        return []
    
    # Parse allergies
    allergy_list = [a.strip().lower() for a in allergies.split(',')] if allergies else []
    
    recommended_medicines = []
    
    for dm in disease_medicines:
        medicine = Medicine.query.get(dm.medicine_id)
        
        # Skip if medicine name is in allergies
        if medicine.name.lower() in allergy_list:
            continue
        
        # Get additional info from OpenFDA API
        openfda_info = get_openfda_info(medicine.name)
        
        # Get drug interactions from RxNorm API
        interactions = get_rxnorm_interactions(medicine.name)
        
        recommended_medicines.append({
            'id': medicine.id,
            'name': medicine.name,
            'description': medicine.description,
            'dosage': openfda_info.get('dosage') or medicine.dosage,
            'side_effects': openfda_info.get('side_effects') or medicine.side_effects,
            'warnings': openfda_info.get('warnings', []),
            'interactions': interactions,
            'primary_treatment': dm.primary_treatment
        })
    
    # Sort by primary treatment first
    recommended_medicines.sort(key=lambda x: x['primary_treatment'], reverse=True)
    
    return recommended_medicines

# Helper function to get drug info from OpenFDA API
def get_openfda_info(drug_name):
    try:
        # OpenFDA API endpoint
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}+OR+openfda.brand_name:{drug_name}&limit=1"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                
                info = {
                    'dosage': result.get('dosage_and_administration', [''])[0],
                    'side_effects': result.get('adverse_reactions', [''])[0],
                    'warnings': result.get('warnings', []) + result.get('boxed_warnings', [])
                }
                
                return info
    except Exception as e:
        print(f"Error fetching OpenFDA data: {e}")
    
    return {}

# Helper function to get drug interactions from RxNorm API
def get_rxnorm_interactions(drug_name):
    try:
        # First get RxCUI for the drug
        rxcui_url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}"
        response = requests.get(rxcui_url)
        
        if response.status_code == 200:
            data = response.json()
            if 'idGroup' in data and 'rxnormId' in data['idGroup'] and len(data['idGroup']['rxnormId']) > 0:
                rxcui = data['idGroup']['rxnormId'][0]
                
                # Get interactions
                interaction_url = f"https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={rxcui}"
                int_response = requests.get(interaction_url)
                
                if int_response.status_code == 200:
                    int_data = int_response.json()
                    interactions = []
                    
                    if 'interactionTypeGroup' in int_data:
                        for group in int_data['interactionTypeGroup']:
                            if 'interactionType' in group:
                                for int_type in group['interactionType']:
                                    if 'interactionPair' in int_type:
                                        for pair in int_type['interactionPair']:
                                            if 'description' in pair:
                                                interactions.append(pair['description'])
                    
                    return interactions
    except Exception as e:
        print(f"Error fetching RxNorm data: {e}")
    
    return []