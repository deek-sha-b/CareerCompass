import unittest
import json
from app import app, db
from models import Career

class SalaryPredictorValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
        
    def test_mismatch_validation(self):
        # Mismatched stream-role: "Software Engineer" with stream "Hotel Management/Vocational"
        response = self.app.post('/api/salary/predict', json={
            'role': 'Software Engineer',
            'stream': 'Hotel Management/Vocational',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'validation_failed')
        self.assertIn('does not match', data.get('message'))
        self.assertIn('Hospitality & Vocational', data.get('message'))
        self.assertIn('Computer Science / IT', data.get('message'))
        
    def test_unrecognized_role(self):
        # Unrecognized role: "astronomer" or "chef"
        response = self.app.post('/api/salary/predict', json={
            'role': 'astronomer',
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'validation_failed')
        self.assertIn('not recognized', data.get('message'))

    def test_valid_prediction(self):
        # Valid stream-role: "Software Engineer" with "Engineering/Technology"
        response = self.app.post('/api/salary/predict', json={
            'role': 'Software Engineer',
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'experience_years': 2.0,
            'skills_count': 5,
            'location_type': 'metro'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_salary_range', data)
        self.assertEqual(data.get('role'), 'Software Engineer')

if __name__ == '__main__':
    unittest.main()
