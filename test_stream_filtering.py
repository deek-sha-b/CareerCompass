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

    def test_zero_cross_domain_pollution_and_tech_restrictions(self):
        from ml.recommender import Recommender
        recommender = Recommender()
        
        careers = Career.query.all()
        career_dicts = [c.to_dict() for c in careers]
        
        jobs = Job.query.all()
        job_dicts = [j.to_dict() for j in jobs]
        
        # 1. User has tech/software skills, stream is Engineering/Technology
        tech_profile = {
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'interests': 'Coding, Systems',
            'current_skills': ['Python', 'SQL', 'Git'],
            'target_goal': 'Software Engineer'
        }
        
        recs = recommender.get_career_recommendations(tech_profile, career_dicts)
        
        # Assert no Civil/Mechanical/Electrical/Manufacturing/Construction/Other non-tech careers are recommended
        for rec in recs:
            title = rec['title']
            self.assertNotIn('Civil/Structural Engineer', title)
            self.assertNotIn('Mechanical Engineer', title)
            self.assertNotIn('Industrial Electrician', title)
            self.assertNotIn('Chartered Accountant', title)
            self.assertNotIn('Doctor', title)
            self.assertNotIn('Pharmacist', title)
            
        # Assert the same for job recommendations
        job_recs = recommender.get_job_recommendations(tech_profile, job_dicts)
        for job in job_recs:
            title = job['title']
            self.assertNotIn('Site Engineer', title)
            self.assertNotIn('Tax Accountant', title)
            self.assertNotIn('Pharmacist', title)
            
        # 2. If the user explicitly has domain-specific skills, the domain career can be recommended
        civil_tech_profile = {
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'interests': 'Construction, Coding',
            'current_skills': ['Python', 'AutoCAD', 'Structural Analysis'],
            'target_goal': 'Civil Engineer'
        }
        recs_civil = recommender.get_career_recommendations(civil_tech_profile, career_dicts)
        titles = [r['title'] for r in recs_civil]
        self.assertTrue(any('Civil' in t for t in titles), f"Civil careers not found in {titles}")

    def test_ranking_by_technical_skill_match_percentage(self):
        from ml.recommender import Recommender
        recommender = Recommender()
        
        careers = Career.query.all()
        career_dicts = [c.to_dict() for c in careers]
        
        # Profile with specific skills
        # Software Engineer requires: 'Python, JavaScript, Data Structures, Algorithms, SQL, Git, Software Design'
        # Overlap with ['Python', 'SQL', 'Git'] is 3 skills.
        profile = {
            'stream': 'Engineering/Technology',
            'qualification': 'Undergraduate',
            'interests': 'Coding',
            'current_skills': ['Python', 'SQL', 'Git'],
            'target_goal': 'Software Engineer'
        }
        
        recs = recommender.get_career_recommendations(profile, career_dicts)
        
        # Verify they are ordered by tech_skill_match_pct descending
        pcts = [r.get('tech_skill_match_pct', 0.0) for r in recs]
        self.assertEqual(pcts, sorted(pcts, reverse=True), f"Careers are not ranked by tech_skill_match_pct descending: {pcts}")
        
        # Verify the same for job recommendations
        jobs = Job.query.all()
        job_dicts = [j.to_dict() for j in jobs]
        job_recs = recommender.get_job_recommendations(profile, job_dicts)
        job_pcts = [j.get('tech_skill_match_pct', 0.0) for j in job_recs]
        self.assertEqual(job_pcts, sorted(job_pcts, reverse=True), f"Jobs are not ranked by tech_skill_match_pct descending: {job_pcts}")

if __name__ == '__main__':
    unittest.main()
