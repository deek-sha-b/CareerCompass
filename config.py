import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'career-guidance-super-secret-key-12345')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-for-career-guidance')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Use MongoDB for document-based storage
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.environ.get('MONGO_DB', 'career_guidance')
    
    # Upload parameters
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
