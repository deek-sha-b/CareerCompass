import unittest
import json
from app import app, db
from models import User, Profile

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # Create user
        self.username = "testuser"
        self.email = "test@example.com"
        self.password = "password123"
        
        # Clean up existing test user if any
        existing = User.query.filter_by(username=self.username).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            
        self.user = User(username=self.username, email=self.email)
        self.user.set_password(self.password)
        db.session.add(self.user)
        db.session.commit()
        
    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()
        self.app_context.pop()
        
    def get_auth_token(self):
        response = self.app.post('/api/auth/login', json={
            'username': self.username,
            'password': self.password
        })
        data = json.loads(response.data)
        return data.get('token')
        
    def test_profile_update(self):
        token = self.get_auth_token()
        self.assertIsNotNone(token)
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        # Verify GET profile
        response = self.app.get('/api/auth/profile', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('username'), self.username)
        
        # Verify PUT profile
        profile_data = {
            'full_name': "Test User Name",
            'age': 25,
            'stream': "Engineering/Technology",
            'qualification': "Undergraduate",
            'current_skills': ["Python", "SQL"],
            'interests': ["Coding"],
            'academic_performance': "GPA: 4.0/4",
            'target_goal': "Software Engineer",
            'experience_years': 2.0,
            'bio': "This is a test bio"
        }
        
        response = self.app.put('/api/auth/profile', headers=headers, json=profile_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('message'), 'Profile updated successfully')
        self.assertEqual(data.get('profile').get('full_name'), "Test User Name")
        
        # Verify GET profile again
        response = self.app.get('/api/auth/profile', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('full_name'), "Test User Name")

    def test_profile_validation_failure(self):
        token = self.get_auth_token()
        self.assertIsNotNone(token)
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        # Save a valid profile first
        valid_profile = {
            'full_name': "Valid User",
            'age': 22,
            'stream': "Engineering/Technology",
            'qualification': "Undergraduate",
            'current_skills': ["Python", "SQL"],
            'interests': ["Coding"],
            'academic_performance': "GPA: 3.5/4",
            'target_goal': "Software Engineer",
            'experience_years': 1.0,
            'bio': "Valid bio"
        }
        response = self.app.put('/api/auth/profile', headers=headers, json=valid_profile)
        self.assertEqual(response.status_code, 200)
        
        # Now try to PUT an invalid profile (unrelated stream/skills/goals)
        invalid_profile = {
            'full_name': "Invalid User",
            'age': 22,
            'stream': "Engineering/Technology",
            'qualification': "Undergraduate",
            'current_skills': ["sewing", "cooking"],
            'interests': ["painting"],
            'academic_performance': "GPA: 3.5/4",
            'target_goal': "chef",
            'experience_years': 1.0,
            'bio': "Invalid bio"
        }
        response = self.app.put('/api/auth/profile', headers=headers, json=invalid_profile)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'validation_failed')
        self.assertIn('match', data.get('message').lower())
        
        # Verify that the profile in the database was NOT updated (remains valid_profile)
        response = self.app.get('/api/auth/profile', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('full_name'), "Valid User")

if __name__ == '__main__':
    unittest.main()
