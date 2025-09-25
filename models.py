from flask_login import UserMixin
from datetime import datetime
from extensions import db

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    histories = db.relationship('PatientHistory', backref='patient', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Symptom model
class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Symptom {self.name}>'

# Disease model
class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    symptoms = db.relationship('DiseaseSymptom', backref='disease', lazy=True)
    medicines = db.relationship('DiseaseMedicine', backref='disease', lazy=True)
    
    def __repr__(self):
        return f'<Disease {self.name}>'

# Medicine model
class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    dosage = db.Column(db.String(200), nullable=True)
    side_effects = db.Column(db.Text, nullable=True)
    diseases = db.relationship('DiseaseMedicine', backref='medicine', lazy=True)
    
    def __repr__(self):
        return f'<Medicine {self.name}>'

# Many-to-many relationship between Disease and Symptom
class DiseaseSymptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), nullable=False)
    weight = db.Column(db.Float, default=1.0)  # Weight for symptom importance in disease prediction

# Many-to-many relationship between Disease and Medicine
class DiseaseMedicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    primary_treatment = db.Column(db.Boolean, default=False)  # Is this a primary treatment?

# Patient History model
class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)  # Stored as comma-separated symptom IDs
    allergies = db.Column(db.Text, nullable=True)  # Stored as comma-separated allergies
    predicted_disease = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=True)
    recommended_medicines = db.Column(db.Text, nullable=True)  # Stored as comma-separated medicine IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    disease = db.relationship('Disease', backref='histories')
    
    def __repr__(self):
        return f'<PatientHistory {self.id}>'