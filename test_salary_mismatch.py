import unittest
import json
from app import app, db
from models import User, Profile, Career

class SalaryPredictorValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create test user
        self.username = "salarytestuser"
        self.email = "salarytest@example.com"
        self.password = "password123"
        
        # Delete all users and profiles with this username to clear any duplicates in MongoDB
        existing_users = User.query.filter_by(username=self.username).all()
        for u in existing_users:
            u.delete()
            
        # Clear mock session active objects cache
        db._active_objects.clear()
        
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        db.session.add(self.user)
        db.session.commit()
        
    def tearDown(self):
        # Clean up all users and profiles created during the test
        existing_users = User.query.filter_by(username=self.username).all()
        for u in existing_users:
            u.delete()
        db._active_objects.clear()
        self.app_context.pop()
        
    def get_auth_headers(self):
        response = self.app.post('/api/auth/login', json={
            'username': self.username,
            'password': self.password
        })
        data = json.loads(response.data)
        token = data.get('token')
        return {'Authorization': f'Bearer {token}'}

    def test_mismatch_validation(self):
        # Set up a profile matching Hotel Management / Culinary
        profile = Profile(
            user_id=self.user.id,
            full_name="Culinary Student",
            stream="Hotel Management/Vocational",
            qualification="Undergraduate",
            current_skills="Culinary Arts, Menu Planning",
            interests="Cooking",
            target_goal="Chef / Culinary Artist"
        )
        db.session.add(profile)
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        # Try to predict "Software Engineer" (unrelated to Culinary profile)
        response = self.app.post('/api/salary/predict', headers=headers, json={
            'role': 'Software Engineer',
            'stream': 'Hotel Management/Vocational',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        if response.status_code != 400:
            print("DEBUG mismatch response:", response.status_code, response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'validation_failed')
        self.assertEqual(
            data.get('message'),
            "This job role does not match your profile recommendations. Please choose a relevant career path."
        )
        
    def test_unrecognized_role(self):
        # Set up profile
        profile = Profile(
            user_id=self.user.id,
            full_name="Tech Student",
            stream="Engineering/Technology",
            qualification="Undergraduate",
            current_skills="Python, SQL",
            interests="Coding",
            target_goal="Software Engineer"
        )
        db.session.add(profile)
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        # Try to predict "Astronomer" (unrecognized and not recommended)
        response = self.app.post('/api/salary/predict', headers=headers, json={
            'role': 'astronomer',
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        if response.status_code != 400:
            print("DEBUG unrecognized response:", response.status_code, response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'validation_failed')
        self.assertEqual(
            data.get('message'),
            "This job role does not match your profile recommendations. Please choose a relevant career path."
        )

    def test_valid_prediction(self):
        # Set up valid tech profile
        profile = Profile(
            user_id=self.user.id,
            full_name="Tech Student",
            stream="Engineering/Technology",
            qualification="Undergraduate",
            current_skills="Python, SQL",
            interests="Coding",
            target_goal="Software Engineer"
        )
        db.session.add(profile)
        db.session.commit()
        
        headers = self.get_auth_headers()
        
        response = self.app.post('/api/salary/predict', headers=headers, json={
            'role': 'Software Engineer',
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        if response.status_code != 200:
            print("DEBUG valid prediction response:", response.status_code, response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_salary_range', data)
        self.assertEqual(data.get('role'), 'Software Engineer')

if __name__ == '__main__':
    unittest.main()
