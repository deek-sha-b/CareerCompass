import unittest
import json
from app import app, db
from models import Career, Job
from ml.recommender import are_streams_compatible

class StreamFilteringTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
        
    def test_are_streams_compatible(self):
        # Engineering and Science/Computer CS should be compatible
        self.assertTrue(are_streams_compatible("Engineering/Technology", "Science/Computer Applications"))
        # Engineering and Commerce should not be compatible
        self.assertFalse(are_streams_compatible("Engineering/Technology", "Commerce/Management"))
        # Hospitality and Commerce should not be compatible
        self.assertFalse(are_streams_compatible("Hotel Management/Vocational", "Commerce/Management"))

    def test_career_recommendations_filtering(self):
        # For a user with Engineering/Technology stream, they should only receive tech/engineering recommendations
        # (e.g. Software Engineer, Data Scientist, Database Administrator)
        # And NOT receive CA (Chartered Accountant) or Doctor
        careers = Career.query.all()
        career_dicts = [c.to_dict() for c in careers]
        
        # Test Recommender directly
        from ml.recommender import Recommender
        recommender = Recommender()
        
        eng_profile = {
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'interests': 'Coding, Systems',
            'current_skills': 'Python, SQL',
            'target_goal': 'Software Engineer'
        }
        recs = recommender.get_career_recommendations(eng_profile, career_dicts)
        
        # Assert all recommendations are compatible with Engineering/Technology
        for rec in recs:
            self.assertTrue(are_streams_compatible('Engineering/Technology', rec['stream']), 
                            f"Career {rec['title']} in stream {rec['stream']} is not compatible with Engineering/Technology")
            self.assertNotIn('Chartered Accountant', rec['title'])
            self.assertNotIn('Doctor', rec['title'])
            
        # For a Commerce/Management stream user
        comm_profile = {
            'stream': 'Commerce/Management',
            'qualification': 'Undergraduate',
            'interests': 'Finance, Accounting',
            'current_skills': 'Taxation, Excel',
            'target_goal': 'Chartered Accountant'
        }
        recs_comm = recommender.get_career_recommendations(comm_profile, career_dicts)
        for rec in recs_comm:
            self.assertTrue(are_streams_compatible('Commerce/Management', rec['stream']),
                            f"Career {rec['title']} in stream {rec['stream']} is not compatible with Commerce/Management")
            self.assertNotIn('Software Engineer', rec['title'])
            self.assertNotIn('Doctor', rec['title'])

    def test_job_recommendations_filtering(self):
        jobs = Job.query.all()
        job_dicts = [j.to_dict() for j in jobs]
        
        from ml.recommender import Recommender
        recommender = Recommender()
        
        # For Engineering student, they should only get software/dev/engineering jobs
        eng_profile = {
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'interests': 'Coding',
            'current_skills': 'Python, SQL',
            'target_goal': 'Software Engineer'
        }
        job_recs = recommender.get_job_recommendations(eng_profile, job_dicts)
        for job in job_recs:
            self.assertNotIn('Tax Accountant', job['title'])
            self.assertNotIn('Pharmacist', job['title'])
            
        # For Commerce student, they should only get CA/finance/HR/accounting jobs
        comm_profile = {
            'stream': 'Commerce/Management',
            'qualification': 'Undergraduate',
            'interests': 'Finance',
            'current_skills': 'Accounting, Excel',
            'target_goal': 'Chartered Accountant (CA)'
        }
        job_recs_comm = recommender.get_job_recommendations(comm_profile, job_dicts)
        for job in job_recs_comm:
            self.assertNotIn('Python Developer', job['title'])
            self.assertNotIn('Site Engineer', job['title'])

if __name__ == '__main__':
    unittest.main()
