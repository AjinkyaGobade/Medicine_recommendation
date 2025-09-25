import pytest
from app import app, db
from models import User, Symptom, Disease, Medicine, PatientHistory

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_route_exists(client):
    response = client.get('/')
    # Home route may redirect or render a template, just check for valid response
    assert response.status_code in (200, 302)

def test_database_creation(client):
    # Check if tables are created
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    assert 'user' in tables or 'User' in tables
    assert 'symptom' in tables or 'Symptom' in tables
    assert 'disease' in tables or 'Disease' in tables
    assert 'medicine' in tables or 'Medicine' in tables
    assert 'patient_history' in tables or 'PatientHistory' in tables

def test_register_route_exists(client):
    response = client.get('/register')
    assert response.status_code in (200, 302)

def test_login_route_exists(client):
    response = client.get('/login')
    assert response.status_code in (200, 302)