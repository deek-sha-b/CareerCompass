from datetime import datetime
import json
from pymongo import MongoClient, ReturnDocument
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

# MongoDB initialization
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
mongo_db_name = os.environ.get('MONGO_DB', 'career_guidance')

client = MongoClient(mongo_uri)
db_conn = client[mongo_db_name]

def get_next_sequence_value(sequence_name):
    result = db_conn['counters'].find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result['sequence_value']

# ----------------- SQLALCHEMY COMPATIBILITY LAYER -----------------
import weakref

class SessionMock:
    def add(self, obj):
        obj.save()
    def flush(self):
        pass
    def rollback(self):
        pass
    def commit(self):
        for obj in list(db._active_objects):
            try:
                obj.save()
            except Exception:
                pass
    def delete(self, obj):
        obj.delete()
    def get(self, model_class, id):
        return model_class.get(id)

class DbMock:
    session = SessionMock()
    _active_objects = weakref.WeakSet()
    
    def register_object(self, obj):
        self._active_objects.add(obj)
        
    def init_app(self, app):
        pass
        
    def create_all(self):
        pass
        
    def drop_all(self):
        for coll in ['users', 'profiles', 'careers', 'jobs', 'courses', 'resumes', 'saved_careers', 'saved_jobs', 'counters']:
            db_conn[coll].drop()
            
    def or_(self, *args):
        conds = []
        for arg in args:
            if isinstance(arg, QueryCondition):
                conds.append(arg.filter_dict)
            elif isinstance(arg, dict):
                conds.append(arg)
        return QueryCondition({"$or": conds})

db = DbMock()

class QueryCondition:
    def __init__(self, filter_dict):
        self.filter_dict = filter_dict
        
    def __or__(self, other):
        conds = []
        for x in [self, other]:
            if isinstance(x, QueryCondition):
                if '$or' in x.filter_dict:
                    conds.extend(x.filter_dict['$or'])
                else:
                    conds.append(x.filter_dict)
            elif isinstance(x, dict):
                conds.append(x)
        return QueryCondition({'$or': conds})
        
    def __and__(self, other):
        conds = []
        for x in [self, other]:
            if isinstance(x, QueryCondition):
                conds.append(x.filter_dict)
            elif isinstance(x, dict):
                conds.append(x)
        return QueryCondition({'$and': conds})

class Field:
    def __init__(self, name):
        self.name = name
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
        
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __eq__(self, other):
        return QueryCondition({self.name: other})
        
    def __ne__(self, other):
        return QueryCondition({self.name: {'$ne': other}})
        
    def like(self, pattern):
        clean_pattern = pattern.strip('%')
        return QueryCondition({self.name: {'$regex': re.escape(clean_pattern), '$options': 'i'}})
        
    def desc(self):
        return (self.name, -1)
        
    def asc(self):
        return (self.name, 1)

class MongoQuery:
    def __init__(self, model_class, filter_dict=None, sort_list=None):
        self.model_class = model_class
        self.filter_dict = filter_dict or {}
        self.sort_list = sort_list or []
        
    def filter_by(self, **kwargs):
        new_filter = {**self.filter_dict, **kwargs}
        return MongoQuery(self.model_class, new_filter, self.sort_list)
        
    def filter(self, *args):
        new_filter = {**self.filter_dict}
        for arg in args:
            filter_dict = arg.filter_dict if isinstance(arg, QueryCondition) else arg
            if isinstance(filter_dict, dict):
                for k, v in filter_dict.items():
                    if k in ['$or', '$and']:
                        if k in new_filter:
                            new_filter = {'$and': [new_filter, {k: v}]}
                        else:
                            new_filter[k] = v
                    else:
                        new_filter[k] = v
        return MongoQuery(self.model_class, new_filter, self.sort_list)
        
    def order_by(self, *args):
        new_sort = list(self.sort_list)
        for arg in args:
            if isinstance(arg, tuple):
                new_sort.append(arg)
            elif isinstance(arg, str):
                new_sort.append((arg, 1))
        return MongoQuery(self.model_class, self.filter_dict, new_sort)
        
    def first(self):
        coll = db_conn[self.model_class.__collection__]
        cursor = coll.find(self.filter_dict)
        if self.sort_list:
            cursor = cursor.sort(self.sort_list)
        docs = list(cursor.limit(1))
        return self.model_class.from_db_doc(docs[0]) if docs else None
        
    def all(self):
        coll = db_conn[self.model_class.__collection__]
        cursor = coll.find(self.filter_dict)
        if self.sort_list:
            cursor = cursor.sort(self.sort_list)
        return [self.model_class.from_db_doc(doc) for doc in cursor]
        
    def count(self):
        coll = db_conn[self.model_class.__collection__]
        return coll.count_documents(self.filter_dict)

class MongoModelMetaclass(type):
    @property
    def query(cls):
        return MongoQuery(cls)

class MongoModel(metaclass=MongoModelMetaclass):
    __collection__ = None
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        for k, v in kwargs.items():
            setattr(self, k, v)
        db.register_object(self)
            
    def save(self):
        coll = db_conn[self.__collection__]
        data = self.to_db_dict()
        if self.id is None:
            self.id = get_next_sequence_value(self.__collection__)
            data['id'] = self.id
            coll.insert_one(data)
        else:
            coll.replace_one({'id': int(self.id)}, data, upsert=True)
            
    def delete(self):
        if self.id is not None:
            db_conn[self.__collection__].delete_one({'id': int(self.id)})
            
    @classmethod
    def get(cls, id):
        if id is None:
            return None
        doc = db_conn[cls.__collection__].find_one({'id': int(id)})
        return cls.from_db_doc(doc) if doc else None

# ----------------- MONGO SCHEMAS / MODEL CLASSES -----------------

class User(MongoModel):
    __collection__ = 'users'
    
    id = Field('id')
    username = Field('username')
    email = Field('email')
    password_hash = Field('password_hash')
    role = Field('role')
    created_at = Field('created_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'role'):
            self.role = 'student'
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.utcnow()
            
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_db_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        
    def delete(self):
        db_conn['profiles'].delete_many({'user_id': int(self.id)})
        db_conn['resumes'].delete_many({'user_id': int(self.id)})
        db_conn['saved_careers'].delete_many({'user_id': int(self.id)})
        db_conn['saved_jobs'].delete_many({'user_id': int(self.id)})
        super().delete()

    @property
    def profile(self):
        return Profile.query.filter_by(user_id=self.id).first()
        
    @property
    def resumes(self):
        return Resume.query.filter_by(user_id=self.id).all()
        
    @property
    def saved_careers(self):
        return SavedCareer.query.filter_by(user_id=self.id).all()
        
    @property
    def saved_jobs(self):
        return SavedJob.query.filter_by(user_id=self.id).all()

class Profile(MongoModel):
    __collection__ = 'profiles'
    
    id = Field('id')
    user_id = Field('user_id')
    full_name = Field('full_name')
    age = Field('age')
    stream = Field('stream')
    qualification = Field('qualification')
    interests = Field('interests')
    current_skills = Field('current_skills')
    academic_performance = Field('academic_performance')
    target_goal = Field('target_goal')
    experience_years = Field('experience_years')
    bio = Field('bio')
    updated_at = Field('updated_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'experience_years'):
            self.experience_years = 0.0
        if not hasattr(self, 'updated_at'):
            self.updated_at = datetime.utcnow()
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': getattr(self, 'full_name', ''),
            'age': getattr(self, 'age', None),
            'stream': getattr(self, 'stream', ''),
            'qualification': getattr(self, 'qualification', ''),
            'interests': getattr(self, 'interests', ''),
            'current_skills': getattr(self, 'current_skills', ''),
            'academic_performance': getattr(self, 'academic_performance', ''),
            'target_goal': getattr(self, 'target_goal', ''),
            'experience_years': getattr(self, 'experience_years', 0.0),
            'bio': getattr(self, 'bio', ''),
            'updated_at': datetime.utcnow()
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        interests_str = getattr(self, 'interests', '')
        skills_str = getattr(self, 'current_skills', '')
        return {
            'user_id': self.user_id,
            'full_name': getattr(self, 'full_name', '') or '',
            'age': getattr(self, 'age', None),
            'stream': getattr(self, 'stream', '') or '',
            'qualification': getattr(self, 'qualification', '') or '',
            'interests': [x.strip() for x in interests_str.split(',')] if interests_str else [],
            'current_skills': [x.strip() for x in skills_str.split(',')] if skills_str else [],
            'academic_performance': getattr(self, 'academic_performance', '') or '',
            'target_goal': getattr(self, 'target_goal', '') or '',
            'experience_years': getattr(self, 'experience_years', 0.0),
            'bio': getattr(self, 'bio', '') or ''
        }

class Career(MongoModel):
    __collection__ = 'careers'
    
    id = Field('id')
    title = Field('title')
    stream = Field('stream')
    description = Field('description')
    required_skills = Field('required_skills')
    min_education = Field('min_education')
    salary_range = Field('salary_range')
    type = Field('type')
    difficulty = Field('difficulty')
    market_demand = Field('market_demand')
    higher_studies_options = Field('higher_studies_options')
    roadmap_steps = Field('roadmap_steps')
    
    def to_db_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'stream': self.stream,
            'description': self.description,
            'required_skills': self.required_skills,
            'min_education': self.min_education,
            'salary_range': self.salary_range,
            'type': self.type,
            'difficulty': self.difficulty,
            'market_demand': self.market_demand,
            'higher_studies_options': self.higher_studies_options,
            'roadmap_steps': self.roadmap_steps
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        roadmap = []
        steps = getattr(self, 'roadmap_steps', '')
        if steps:
            if isinstance(steps, str):
                try:
                    roadmap = json.loads(steps)
                except Exception:
                    roadmap = []
            elif isinstance(steps, list):
                roadmap = steps
                
        skills_str = getattr(self, 'required_skills', '')
        higher_str = getattr(self, 'higher_studies_options', '')
        return {
            'id': self.id,
            'title': self.title,
            'stream': self.stream,
            'description': self.description,
            'required_skills': [x.strip() for x in skills_str.split(',')] if isinstance(skills_str, str) else (skills_str or []),
            'min_education': self.min_education,
            'salary_range': self.salary_range,
            'type': self.type,
            'difficulty': self.difficulty,
            'market_demand': self.market_demand,
            'higher_studies_options': [x.strip() for x in higher_str.split(',')] if isinstance(higher_str, str) else (higher_str or []),
            'roadmap_steps': roadmap
        }

class Job(MongoModel):
    __collection__ = 'jobs'
    
    id = Field('id')
    title = Field('title')
    company = Field('company')
    description = Field('description')
    type = Field('type')
    location = Field('location')
    skills_required = Field('skills_required')
    salary = Field('salary')
    experience_required = Field('experience_required')
    link = Field('link')
    created_at = Field('created_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'experience_required'):
            self.experience_required = 0.0
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'type': self.type,
            'location': self.location,
            'skills_required': self.skills_required,
            'salary': self.salary,
            'experience_required': self.experience_required,
            'link': self.link,
            'created_at': self.created_at
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        skills_str = getattr(self, 'skills_required', '')
        created_val = getattr(self, 'created_at', None)
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'type': self.type,
            'location': self.location,
            'skills_required': [x.strip() for x in skills_str.split(',')] if isinstance(skills_str, str) else (skills_str or []),
            'salary': self.salary,
            'experience_required': self.experience_required,
            'link': self.link or '#',
            'created_at': created_val.isoformat() if isinstance(created_val, datetime) else created_val
        }

class Course(MongoModel):
    __collection__ = 'courses'
    
    id = Field('id')
    title = Field('title')
    provider = Field('provider')
    platform = Field('platform')
    skill_category = Field('skill_category')
    difficulty = Field('difficulty')
    duration = Field('duration')
    rating = Field('rating')
    link = Field('link')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'rating'):
            self.rating = 4.5
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'provider': self.provider,
            'platform': self.platform,
            'skill_category': self.skill_category,
            'difficulty': self.difficulty,
            'duration': self.duration,
            'rating': self.rating,
            'link': self.link
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'provider': getattr(self, 'provider', '') or '',
            'platform': getattr(self, 'platform', '') or '',
            'skill_category': self.skill_category,
            'difficulty': self.difficulty,
            'duration': self.duration,
            'rating': self.rating,
            'link': self.link or '#'
        }



class Resume(MongoModel):
    __collection__ = 'resumes'
    
    id = Field('id')
    user_id = Field('user_id')
    template_name = Field('template_name')
    name = Field('name')
    email = Field('email')
    phone = Field('phone')
    location = Field('location')
    summary = Field('summary')
    education = Field('education')
    skills = Field('skills')
    experience = Field('experience')
    projects = Field('projects')
    certifications = Field('certifications')
    achievements = Field('achievements')
    ats_score = Field('ats_score')
    feedback = Field('feedback')
    created_at = Field('created_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'template_name'):
            self.template_name = 'Modern Minimalist'
        if not hasattr(self, 'ats_score'):
            self.ats_score = 0
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'template_name': self.template_name,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'education': self.education,
            'skills': self.skills,
            'experience': self.experience,
            'projects': self.projects,
            'certifications': self.certifications,
            'achievements': self.achievements,
            'ats_score': self.ats_score,
            'feedback': self.feedback,
            'created_at': self.created_at
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    def to_dict(self):
        def parse_json(field_val):
            if not field_val:
                return []
            if isinstance(field_val, str):
                try:
                    return json.loads(field_val)
                except Exception:
                    return []
            return field_val
            
        def parse_json_dict(field_val):
            if not field_val:
                return {}
            if isinstance(field_val, str):
                try:
                    return json.loads(field_val)
                except Exception:
                    return {}
            return field_val
            
        skills_str = getattr(self, 'skills', '')
        certs_str = getattr(self, 'certifications', '')
        ach_str = getattr(self, 'achievements', '')
        created_val = getattr(self, 'created_at', None)
        
        return {
            'id': self.id,
            'template_name': self.template_name,
            'name': self.name,
            'email': self.email,
            'phone': self.phone or '',
            'location': self.location or '',
            'summary': self.summary or '',
            'education': parse_json(self.education),
            'skills': [x.strip() for x in skills_str.split(',')] if isinstance(skills_str, str) else (skills_str or []),
            'experience': parse_json(self.experience),
            'projects': parse_json(self.projects),
            'certifications': [x.strip() for x in certs_str.split(',')] if isinstance(certs_str, str) else (certs_str or []),
            'achievements': [x.strip() for x in ach_str.split(',')] if isinstance(ach_str, str) else (ach_str or []),
            'ats_score': self.ats_score,
            'feedback': parse_json_dict(self.feedback),
            'created_at': created_val.isoformat() if isinstance(created_val, datetime) else created_val
        }

class SavedCareer(MongoModel):
    __collection__ = 'saved_careers'
    
    id = Field('id')
    user_id = Field('user_id')
    career_id = Field('career_id')
    saved_at = Field('saved_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'saved_at'):
            self.saved_at = datetime.utcnow()
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'career_id': self.career_id,
            'saved_at': self.saved_at
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    @property
    def career(self):
        return Career.query.filter_by(id=self.career_id).first()

class SavedJob(MongoModel):
    __collection__ = 'saved_jobs'
    
    id = Field('id')
    user_id = Field('user_id')
    job_id = Field('job_id')
    saved_at = Field('saved_at')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'saved_at'):
            self.saved_at = datetime.utcnow()
            
    def to_db_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'saved_at': self.saved_at
        }
        
    @classmethod
    def from_db_doc(cls, doc):
        return cls(**doc)
        
    @property
    def job(self):
        return Job.query.filter_by(id=self.job_id).first()
