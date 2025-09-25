from app import app
from extensions import db
from models import User, Symptom, Disease, Medicine, DiseaseSymptom, DiseaseMedicine
from werkzeug.security import generate_password_hash

def seed_database():
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('admin123', method='sha256')
    )
    db.session.add(admin)
    
    # Create symptoms
    symptoms = [
        Symptom(name='Fever', description='Body temperature above normal'),
        Symptom(name='Cough', description='Sudden expulsion of air from the lungs'),
        Symptom(name='Headache', description='Pain in the head or upper neck'),
        Symptom(name='Fatigue', description='Extreme tiredness resulting from mental or physical exertion'),
        Symptom(name='Sore Throat', description='Pain or irritation in the throat'),
        Symptom(name='Runny Nose', description='Excess discharge of fluid from the nose'),
        Symptom(name='Shortness of Breath', description='Difficulty breathing or catching your breath'),
        Symptom(name='Chest Pain', description='Pain or discomfort in the chest'),
        Symptom(name='Nausea', description='Feeling of sickness with an inclination to vomit'),
        Symptom(name='Vomiting', description='Forcible voluntary or involuntary emptying of stomach contents through the mouth'),
        Symptom(name='Diarrhea', description='Loose, watery stools occurring more frequently than usual'),
        Symptom(name='Muscle Pain', description='Pain affecting the muscles'),
        Symptom(name='Joint Pain', description='Discomfort that arises from any joint'),
        Symptom(name='Rash', description='Area of irritated or swollen skin'),
        Symptom(name='Chills', description='Feeling of coldness accompanied by shivering'),
        Symptom(name='Dizziness', description='Lightheadedness, feeling faint or unsteady'),
        Symptom(name='Loss of Taste or Smell', description='Inability to taste or smell'),
        Symptom(name='Abdominal Pain', description='Pain that occurs between the chest and pelvic regions'),
        Symptom(name='Swollen Lymph Nodes', description='Enlarged lymph nodes'),
        Symptom(name='High Blood Pressure', description='Blood pressure that is higher than normal')
    ]
    
    for symptom in symptoms:
        db.session.add(symptom)
    
    # Create diseases
    diseases = [
        Disease(name='Common Cold', description='A viral infectious disease of the upper respiratory tract'),
        Disease(name='Influenza', description='A viral infection that attacks your respiratory system'),
        Disease(name='COVID-19', description='A respiratory illness caused by the SARS-CoV-2 virus'),
        Disease(name='Hypertension', description='High blood pressure'),
        Disease(name='Migraine', description='A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound'),
        Disease(name='Gastroenteritis', description='Inflammation of the stomach and intestines'),
        Disease(name='Bronchitis', description='Inflammation of the lining of the bronchial tubes'),
        Disease(name='Pneumonia', description='Infection that inflames air sacs in one or both lungs'),
        Disease(name='Allergic Rhinitis', description='Allergic response causing cold-like symptoms'),
        Disease(name='Urinary Tract Infection', description='Infection in any part of the urinary system')
    ]
    
    for disease in diseases:
        db.session.add(disease)
    
    # Commit to get IDs
    db.session.commit()
    
    # Create medicines
    medicines = [
        Medicine(name='Acetaminophen', description='Pain reliever and fever reducer', 
                dosage='Adults: 325-650 mg every 4-6 hours as needed', 
                side_effects='Rare: liver damage with high doses'),
        Medicine(name='Ibuprofen', description='Nonsteroidal anti-inflammatory drug (NSAID)', 
                dosage='Adults: 200-400 mg every 4-6 hours as needed', 
                side_effects='Stomach upset, heartburn, may increase risk of heart attack and stroke'),
        Medicine(name='Amoxicillin', description='Penicillin antibiotic', 
                dosage='Adults: 250-500 mg three times daily', 
                side_effects='Diarrhea, rash, nausea, vomiting'),
        Medicine(name='Loratadine', description='Antihistamine for allergy relief', 
                dosage='Adults: 10 mg once daily', 
                side_effects='Headache, drowsiness, dry mouth'),
        Medicine(name='Lisinopril', description='ACE inhibitor for high blood pressure', 
                dosage='Adults: 10-40 mg once daily', 
                side_effects='Dry cough, dizziness, headache'),
        Medicine(name='Azithromycin', description='Macrolide antibiotic', 
                dosage='Adults: 500 mg on day 1, then 250 mg daily for 4 days', 
                side_effects='Diarrhea, nausea, abdominal pain'),
        Medicine(name='Sumatriptan', description='Triptan for migraine relief', 
                dosage='Adults: 25-100 mg at onset of migraine', 
                side_effects='Tingling, warm sensations, dizziness'),
        Medicine(name='Oseltamivir', description='Antiviral for influenza', 
                dosage='Adults: 75 mg twice daily for 5 days', 
                side_effects='Nausea, vomiting, headache'),
        Medicine(name='Loperamide', description='Anti-diarrheal', 
                dosage='Adults: 4 mg initially, then 2 mg after each loose stool', 
                side_effects='Constipation, dry mouth, abdominal discomfort'),
        Medicine(name='Albuterol', description='Bronchodilator for breathing problems', 
                dosage='Adults: 1-2 inhalations every 4-6 hours as needed', 
                side_effects='Tremor, nervousness, headache')
    ]
    
    for medicine in medicines:
        db.session.add(medicine)
    
    # Commit to get IDs
    db.session.commit()
    
    # Map symptoms to diseases with weights
    disease_symptoms = [
        # Common Cold
        DiseaseSymptom(disease_id=1, symptom_id=1, weight=0.7),  # Fever
        DiseaseSymptom(disease_id=1, symptom_id=2, weight=0.9),  # Cough
        DiseaseSymptom(disease_id=1, symptom_id=5, weight=0.8),  # Sore Throat
        DiseaseSymptom(disease_id=1, symptom_id=6, weight=1.0),  # Runny Nose
        
        # Influenza
        DiseaseSymptom(disease_id=2, symptom_id=1, weight=1.0),  # Fever
        DiseaseSymptom(disease_id=2, symptom_id=2, weight=0.8),  # Cough
        DiseaseSymptom(disease_id=2, symptom_id=4, weight=1.0),  # Fatigue
        DiseaseSymptom(disease_id=2, symptom_id=12, weight=0.9),  # Muscle Pain
        DiseaseSymptom(disease_id=2, symptom_id=15, weight=0.7),  # Chills
        
        # COVID-19
        DiseaseSymptom(disease_id=3, symptom_id=1, weight=0.8),  # Fever
        DiseaseSymptom(disease_id=3, symptom_id=2, weight=0.9),  # Cough
        DiseaseSymptom(disease_id=3, symptom_id=4, weight=0.7),  # Fatigue
        DiseaseSymptom(disease_id=3, symptom_id=7, weight=0.8),  # Shortness of Breath
        DiseaseSymptom(disease_id=3, symptom_id=17, weight=1.0),  # Loss of Taste or Smell
        
        # Hypertension
        DiseaseSymptom(disease_id=4, symptom_id=3, weight=0.6),  # Headache
        DiseaseSymptom(disease_id=4, symptom_id=16, weight=0.7),  # Dizziness
        DiseaseSymptom(disease_id=4, symptom_id=20, weight=1.0),  # High Blood Pressure
        
        # Migraine
        DiseaseSymptom(disease_id=5, symptom_id=3, weight=1.0),  # Headache
        DiseaseSymptom(disease_id=5, symptom_id=9, weight=0.6),  # Nausea
        DiseaseSymptom(disease_id=5, symptom_id=16, weight=0.7),  # Dizziness
        
        # Gastroenteritis
        DiseaseSymptom(disease_id=6, symptom_id=9, weight=0.9),  # Nausea
        DiseaseSymptom(disease_id=6, symptom_id=10, weight=0.8),  # Vomiting
        DiseaseSymptom(disease_id=6, symptom_id=11, weight=1.0),  # Diarrhea
        DiseaseSymptom(disease_id=6, symptom_id=18, weight=0.7),  # Abdominal Pain
        
        # Bronchitis
        DiseaseSymptom(disease_id=7, symptom_id=2, weight=1.0),  # Cough
        DiseaseSymptom(disease_id=7, symptom_id=4, weight=0.6),  # Fatigue
        DiseaseSymptom(disease_id=7, symptom_id=7, weight=0.8),  # Shortness of Breath
        DiseaseSymptom(disease_id=7, symptom_id=8, weight=0.7),  # Chest Pain
        
        # Pneumonia
        DiseaseSymptom(disease_id=8, symptom_id=1, weight=0.9),  # Fever
        DiseaseSymptom(disease_id=8, symptom_id=2, weight=0.8),  # Cough
        DiseaseSymptom(disease_id=8, symptom_id=7, weight=1.0),  # Shortness of Breath
        DiseaseSymptom(disease_id=8, symptom_id=8, weight=0.9),  # Chest Pain
        DiseaseSymptom(disease_id=8, symptom_id=15, weight=0.6),  # Chills
        
        # Allergic Rhinitis
        DiseaseSymptom(disease_id=9, symptom_id=6, weight=1.0),  # Runny Nose
        DiseaseSymptom(disease_id=9, symptom_id=14, weight=0.6),  # Rash
        
        # Urinary Tract Infection
        DiseaseSymptom(disease_id=10, symptom_id=1, weight=0.6),  # Fever
        DiseaseSymptom(disease_id=10, symptom_id=18, weight=0.8)  # Abdominal Pain
    ]
    
    for ds in disease_symptoms:
        db.session.add(ds)
    
    # Map medicines to diseases
    disease_medicines = [
        # Common Cold
        DiseaseMedicine(disease_id=1, medicine_id=1, primary_treatment=True),  # Acetaminophen
        DiseaseMedicine(disease_id=1, medicine_id=2, primary_treatment=False),  # Ibuprofen
        DiseaseMedicine(disease_id=1, medicine_id=4, primary_treatment=False),  # Loratadine
        
        # Influenza
        DiseaseMedicine(disease_id=2, medicine_id=1, primary_treatment=True),  # Acetaminophen
        DiseaseMedicine(disease_id=2, medicine_id=2, primary_treatment=False),  # Ibuprofen
        DiseaseMedicine(disease_id=2, medicine_id=8, primary_treatment=True),  # Oseltamivir
        
        # COVID-19
        DiseaseMedicine(disease_id=3, medicine_id=1, primary_treatment=True),  # Acetaminophen
        DiseaseMedicine(disease_id=3, medicine_id=2, primary_treatment=False),  # Ibuprofen
        
        # Hypertension
        DiseaseMedicine(disease_id=4, medicine_id=5, primary_treatment=True),  # Lisinopril
        
        # Migraine
        DiseaseMedicine(disease_id=5, medicine_id=1, primary_treatment=False),  # Acetaminophen
        DiseaseMedicine(disease_id=5, medicine_id=2, primary_treatment=False),  # Ibuprofen
        DiseaseMedicine(disease_id=5, medicine_id=7, primary_treatment=True),  # Sumatriptan
        
        # Gastroenteritis
        DiseaseMedicine(disease_id=6, medicine_id=9, primary_treatment=True),  # Loperamide
        
        # Bronchitis
        DiseaseMedicine(disease_id=7, medicine_id=3, primary_treatment=True),  # Amoxicillin
        DiseaseMedicine(disease_id=7, medicine_id=10, primary_treatment=False),  # Albuterol
        
        # Pneumonia
        DiseaseMedicine(disease_id=8, medicine_id=3, primary_treatment=True),  # Amoxicillin
        DiseaseMedicine(disease_id=8, medicine_id=6, primary_treatment=True),  # Azithromycin
        
        # Allergic Rhinitis
        DiseaseMedicine(disease_id=9, medicine_id=4, primary_treatment=True),  # Loratadine
        
        # Urinary Tract Infection
        DiseaseMedicine(disease_id=10, medicine_id=3, primary_treatment=True)  # Amoxicillin
    ]
    
    for dm in disease_medicines:
        db.session.add(dm)
    
    # Commit all changes
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if database is already seeded
        if User.query.count() == 0:
            seed_database()
        else:
            print("Database already contains data. Skipping seed.")