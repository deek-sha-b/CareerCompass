import re
import math
import os
import pickle

# Try importing numpy and scikit-learn for advanced mode, but fallback to pure Python
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def get_stream_ui_name(db_stream):
    if not db_stream:
        return "Unknown"
    db_stream = db_stream.lower()
    if 'hotel' in db_stream or 'vocational' in db_stream:
        return "Hospitality & Vocational"
    elif 'engineering' in db_stream or 'technology' in db_stream or 'computer' in db_stream or 'science' in db_stream:
        return "Computer Science / IT"
    elif 'commerce' in db_stream or 'management' in db_stream:
        return "Commerce / Management"
    elif 'design' in db_stream or 'art' in db_stream:
        return "Design / Arts"
    elif 'law' in db_stream:
        return "Law"
    elif 'medical' in db_stream or 'pharmacy' in db_stream:
        return "Medical / Pharmacy"
    elif 'education' in db_stream or 'humanities' in db_stream:
        return "Humanities / Arts"
    else:
        return db_stream.title()

def get_stream_related_field(db_stream):
    if not db_stream:
        return "other fields"
    db_stream = db_stream.lower()
    if 'agriculture' in db_stream:
        return "Agriculture"
    elif 'engineering' in db_stream or 'technology' in db_stream or 'computer' in db_stream or 'science' in db_stream:
        return "Software Development"
    elif 'hotel' in db_stream or 'vocational' in db_stream:
        return "Hospitality"
    elif 'commerce' in db_stream or 'management' in db_stream:
        return "Commerce & Management"
    elif 'design' in db_stream or 'art' in db_stream:
        return "Design & Creative Arts"
    elif 'law' in db_stream:
        return "Legal Services"
    elif 'medical' in db_stream or 'pharmacy' in db_stream:
        return "Medical & Pharmacy"
    elif 'education' in db_stream or 'humanities' in db_stream:
        return "Education & Humanities"
    else:
        return "other fields"

def are_streams_compatible(stream1, stream2):
    if not stream1 or not stream2:
        return False
        
    s1_lower = stream1.lower().strip()
    s2_lower = stream2.lower().strip()
    
    # 1. Exact match
    if s1_lower == s2_lower:
        return True
        
    # 2. Map to the same high-level industry field (excluding "other fields")
    field1 = get_stream_related_field(stream1)
    field2 = get_stream_related_field(stream2)
    if field1 != "other fields" and field1 == field2:
        return True
        
    return False

def is_job_compatible_with_stream(job, user_stream, careers, recommender):
    if not user_stream:
        return True
        
    # Find closest matching career for the job using Recommender TF-IDF Cosine Similarity
    career_docs = []
    for career in careers:
        career_skills = ", ".join(career.get('required_skills', [])) if isinstance(career.get('required_skills'), list) else str(career.get('required_skills', ''))
        doc = f"{career.get('title', '')} {career.get('description', '')} {career_skills}"
        career_docs.append(doc)
        
    job_skills_raw = job.get('skills_required', [])
    job_skills_str = ", ".join(job_skills_raw) if isinstance(job_skills_raw, list) else str(job_skills_raw)
    job_doc = f"{job.get('title', '')} {job.get('description', '')} {job_skills_str}"
    
    sims = recommender._pure_python_tfidf_cosine_similarity(job_doc, career_docs)
    max_sim = max(sims) if sims else 0.0
    if max_sim < 0.05:
        # Fallback if no matching career found
        return True
        
    best_idx = sims.index(max_sim)
    closest_career = careers[best_idx]
    
    return are_streams_compatible(user_stream, closest_career.get('stream', ''))


class Recommender:
    def __init__(self):
        self.has_sklearn = HAS_SKLEARN
        self.vectorizer = None
        
        # Load serialized TF-IDF vectorizer if available
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vectorizer_path = os.path.join(base_dir, 'ml', 'recommender_vectorizer.pkl')
        
        if self.has_sklearn:
            try:
                if os.path.exists(vectorizer_path):
                    with open(vectorizer_path, 'rb') as f:
                        self.vectorizer = pickle.load(f)
                    print(f"[Recommender] Serialized TF-IDF vectorizer loaded successfully from {vectorizer_path}")
            except Exception as e:
                print(f"[Recommender] Error loading serialized vectorizer: {e}. Falling back to dynamic fitting.")

    def _clean_text(self, text):
        if not text:
            return ""
        # Lowecase, remove non-alphanumeric
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s,]', '', text)
        return text

    def _pure_python_tfidf_cosine_similarity(self, query_text, docs):
        """
        Pure Python TF-IDF and Cosine Similarity implementation.
        Zero dependencies. Highly reliable and performant for mock-sized data.
        """
        query_text = self._clean_text(query_text)
        cleaned_docs = [self._clean_text(doc) for doc in docs]
        
        # 1. Tokenize into words
        def tokenize(text):
            return [w for w in re.split(r'\s+', text) if len(w) > 1]
        
        query_tokens = tokenize(query_text)
        doc_tokens_list = [tokenize(doc) for doc in cleaned_docs]
        all_tokens = query_tokens + [tok for doc_toks in doc_tokens_list for tok in doc_toks]
        vocabulary = list(set(all_tokens))
        
        if not vocabulary or not docs:
            return [0.0] * len(docs)
            
        vocab_index = {word: i for i, word in enumerate(vocabulary)}
        N = len(docs) + 1  # Total docs including query
        
        # 2. Calculate Document Frequency (DF)
        df = {word: 0 for word in vocabulary}
        # Count in query
        query_set = set(query_tokens)
        for word in query_set:
            df[word] += 1
        # Count in docs
        for doc_toks in doc_tokens_list:
            doc_set = set(doc_toks)
            for word in doc_set:
                if word in df:
                    df[word] += 1
                    
        # 3. Calculate IDF
        idf = {}
        for word, count in df.items():
            # Smooth IDF
            idf[word] = math.log(N / (count or 1)) + 1.0

        # Helper to compute tf-idf vector
        def get_tfidf_vector(tokens):
            tf = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            
            vector = [0.0] * len(vocabulary)
            for token, freq in tf.items():
                if token in vocab_index:
                    # Log-frequency TF * IDF
                    tf_val = 1 + math.log(freq) if freq > 0 else 0
                    vector[vocab_index[token]] = tf_val * idf[token]
            return vector

        # Compute vectors
        query_vec = get_tfidf_vector(query_tokens)
        doc_vectors = [get_tfidf_vector(doc_toks) for doc_toks in doc_tokens_list]
        
        # Helper to compute Cosine Similarity
        def cosine_sim(v1, v2):
            dot_product = sum(a * b for a, b in zip(v1, v2))
            mag1 = math.sqrt(sum(a * a for a in v1))
            mag2 = math.sqrt(sum(b * b for b in v2))
            if mag1 == 0 or mag2 == 0:
                return 0.0
            return dot_product / (mag1 * mag2)

        # Return list of similarities
        return [cosine_sim(query_vec, doc_vec) for doc_vec in doc_vectors]

    def get_career_recommendations(self, profile, careers, limit=5):
        """
        Recommends careers based on profile details using TF-IDF cosine similarity.
        """
        if not careers:
            return []
            
        # Build user vector context from qualifications, stream, interests, skills, and goals
        user_interests = ", ".join(profile.get('interests', [])) if isinstance(profile.get('interests'), list) else str(profile.get('interests', ''))
        user_skills = ", ".join(profile.get('current_skills', [])) if isinstance(profile.get('current_skills'), list) else str(profile.get('current_skills', ''))
        query = f"{profile.get('stream', '')} {profile.get('qualification', '')} {user_interests} {user_skills} {profile.get('target_goal', '')}"
        
        # Build document text from Careers
        career_docs = []
        for career in careers:
            career_skills = ", ".join(career.get('required_skills', [])) if isinstance(career.get('required_skills'), list) else str(career.get('required_skills', ''))
            higher_options = ", ".join(career.get('higher_studies_options', [])) if isinstance(career.get('higher_studies_options'), list) else str(career.get('higher_studies_options', ''))
            doc = f"{career.get('title', '')} {career.get('stream', '')} {career.get('description', '')} {career_skills} {career.get('min_education', '')} {higher_options}"
            career_docs.append(doc)
            
        # 1. Stream Validation (if stream is provided)
        p_stream = profile.get('stream', '').strip()
        if p_stream:
            p_tokens = set(re.split(r'[^a-zA-Z0-9]+', p_stream.lower()))
            p_tokens = {t for t in p_tokens if len(t) > 2}
            
            stream_matched = False
            for career in careers:
                c_stream = career.get('stream', '')
                if c_stream:
                    c_tokens = set(re.split(r'[^a-zA-Z0-9]+', c_stream.lower()))
                    c_tokens = {t for t in c_tokens if len(t) > 2}
                    if p_tokens.intersection(c_tokens):
                        stream_matched = True
                        break
            if not stream_matched:
                return {
                    'status': 'invalid',
                    'message': 'Insufficient Data Match',
                    'warning_details': 'The entered educational stream is not recognized or does not align with any available career paths.',
                    'suggested_actions': ['Please input a valid educational stream.']
                }

        # 2. Check if the user has provided any custom text fields (free text)
        user_free_text = f"{user_interests} {user_skills} {profile.get('target_goal', '')}".strip()
        has_user_inputs = len(user_free_text) > 0
        
        goal_passed = True
        skills_passed = True
        
        if has_user_inputs:
            # Filter careers that match the user's stream
            stream_career_docs = []
            p_stream = profile.get('stream', '').strip()
            if p_stream:
                p_tokens = set(re.split(r'[^a-zA-Z0-9]+', p_stream.lower()))
                p_tokens = {t for t in p_tokens if len(t) > 2}
                
                for idx, career in enumerate(careers):
                    c_stream = career.get('stream', '')
                    if c_stream:
                        c_tokens = set(re.split(r'[^a-zA-Z0-9]+', c_stream.lower()))
                        c_tokens = {t for t in c_tokens if len(t) > 2}
                        if p_tokens.intersection(c_tokens):
                            stream_career_docs.append(career_docs[idx])
                            
            target_docs = stream_career_docs if stream_career_docs else career_docs
            
            user_goal = profile.get('target_goal', '').strip()
            user_skills_interests = f"{user_interests} {user_skills}".strip()
            
            # Validate Target Goal
            if user_goal:
                if self.has_sklearn and self.vectorizer is not None:
                    try:
                        goal_vec = self.vectorizer.transform([user_goal.lower()])
                        career_vecs = self.vectorizer.transform(target_docs)
                        goal_sims = cosine_similarity(goal_vec, career_vecs).flatten()
                        max_goal_sim = float(np.max(goal_sims)) if len(goal_sims) > 0 else 0.0
                    except Exception:
                        max_goal_sim = 0.0
                else:
                    try:
                        goal_sims = self._pure_python_tfidf_cosine_similarity(user_goal, target_docs)
                        max_goal_sim = max(goal_sims) if goal_sims else 0.0
                    except Exception:
                        max_goal_sim = 0.0
                
                if max_goal_sim < 0.05:
                    goal_passed = False
            
            # Validate Skills and Interests
            if user_skills_interests:
                if self.has_sklearn and self.vectorizer is not None:
                    try:
                        skills_vec = self.vectorizer.transform([user_skills_interests.lower()])
                        career_vecs = self.vectorizer.transform(target_docs)
                        skills_sims = cosine_similarity(skills_vec, career_vecs).flatten()
                        max_skills_sim = float(np.max(skills_sims)) if len(skills_sims) > 0 else 0.0
                    except Exception:
                        max_skills_sim = 0.0
                else:
                    try:
                        skills_sims = self._pure_python_tfidf_cosine_similarity(user_skills_interests, target_docs)
                        max_skills_sim = max(skills_sims) if skills_sims else 0.0
                    except Exception:
                        max_skills_sim = 0.0
                
                if max_skills_sim < 0.05:
                    skills_passed = False
            
        # Run Vector Space Matching
        if self.has_sklearn:
            try:
                if self.vectorizer is not None:
                    query_vec = self.vectorizer.transform([query.lower()])
                    career_vecs = self.vectorizer.transform(career_docs)
                    similarities = cosine_similarity(query_vec, career_vecs).flatten()
                else:
                    vectorizer = TfidfVectorizer(stop_words='english')
                    tfidf_matrix = vectorizer.fit_transform([query] + career_docs)
                    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            except Exception as e:
                print(f"[Recommender] Sklearn career matching failed: {e}. Falling back to pure Python.")
                similarities = self._pure_python_tfidf_cosine_similarity(query, career_docs)
        else:
            similarities = self._pure_python_tfidf_cosine_similarity(query, career_docs)
            
        # Rank recommendations
        ranked_careers = []
        for idx, score in enumerate(similarities):
            # Calculate stream match using token overlap (e.g. 'Humanities/Arts' matches 'Design/Arts')
            p_stream = profile.get('stream', '')
            c_stream = careers[idx].get('stream', '')
            
            is_stream_matched = False
            if p_stream and c_stream:
                p_tokens = set(re.split(r'[^a-zA-Z0-9]+', p_stream.lower()))
                c_tokens = set(re.split(r'[^a-zA-Z0-9]+', c_stream.lower()))
                # Filter out small terms
                p_tokens = {t for t in p_tokens if len(t) > 2}
                c_tokens = {t for t in c_tokens if len(t) > 2}
                if p_tokens.intersection(c_tokens):
                    is_stream_matched = True
            
            stream_match = 1.35 if is_stream_matched else 1.0
            
            # Map similarity score (0.0 to 1.0) into a percentage scale
            base_score = float(score) * 100
            
            # Apply smart baseline score if stream aligns, so empty profiles get helpful suggestions
            # Bypassed if goal or skills validation failed (to force match score below 60)
            if is_stream_matched and goal_passed and skills_passed:
                base_score = max(base_score, 65.0 + (score * 15.0))
            elif p_stream:
                # Penalty for stream mismatch
                base_score = base_score * 0.4
            else:
                # No stream set, use general baseline
                base_score = max(base_score, 45.0 + (score * 10.0))
                
            # Boost score slightly if user's skills overlap with career skills
            user_skills = set(s.lower().strip() for s in profile.get('current_skills', []))
            career_skills = set(s.lower().strip() for s in careers[idx].get('required_skills', []))
            if career_skills and user_skills:
                overlap = user_skills.intersection(career_skills)
                if overlap:
                    overlap_ratio = len(overlap) / len(career_skills)
                    base_score += (overlap_ratio * 15.0)

            final_score = round(base_score * stream_match, 1)
            # Cap at 100
            final_score = min(final_score, 100.0)
            
            career_entry = careers[idx].copy()
            career_entry['match_score'] = final_score
            ranked_careers.append(career_entry)
            
        # Determine maximum confidence score among matching stream careers
        max_confidence_score = 0.0
        p_stream = profile.get('stream', '').strip()
        stream_matched_careers = []
        if p_stream:
            p_tokens = set(re.split(r'[^a-zA-Z0-9]+', p_stream.lower()))
            p_tokens = {t for t in p_tokens if len(t) > 2}
            for c in ranked_careers:
                c_stream = c.get('stream', '')
                if c_stream:
                    c_tokens = set(re.split(r'[^a-zA-Z0-9]+', c_stream.lower()))
                    c_tokens = {t for t in c_tokens if len(t) > 2}
                    if p_tokens.intersection(c_tokens):
                        stream_matched_careers.append(c)
        if stream_matched_careers:
            max_confidence_score = max(c['match_score'] for c in stream_matched_careers)
        else:
            max_confidence_score = 0.0

        # If confidence is below 60%, return warning and suggested actions
        if max_confidence_score < 60.0 or not goal_passed or not skills_passed:
            # Find the best overall matching career from all careers
            best_overall_idx = -1
            best_overall_sim = -1.0
            for i, score in enumerate(similarities):
                if score > best_overall_sim:
                    best_overall_sim = score
                    best_overall_idx = i
            if best_overall_idx != -1:
                best_overall_career = careers[best_overall_idx]
            else:
                best_overall_career = careers[0]

            selected_stream_ui = get_stream_ui_name(profile.get('stream', ''))
            actual_stream_ui = get_stream_ui_name(best_overall_career.get('stream', ''))
            actual_field = get_stream_related_field(best_overall_career.get('stream', ''))
            selected_related_field = get_stream_related_field(profile.get('stream', ''))

            return {
                'status': 'invalid',
                'message': 'Insufficient Data Match',
                'warning_details': f"Your selected education stream is {selected_stream_ui}, but your skills and career goal are related to {actual_field}.",
                'suggested_actions': [
                    f"Change Education Stream to {actual_stream_ui}",
                    f"Or select {selected_related_field}-related career goals"
                ]
            }

        # Filter career recommendations strictly by stream compatibility
        p_stream = profile.get('stream', '').strip()
        if p_stream:
            compatible_careers = []
            for c in ranked_careers:
                c_stream = c.get('stream', '')
                if are_streams_compatible(p_stream, c_stream):
                    compatible_careers.append(c)
            ranked_careers = compatible_careers

        # Sort by match score descending
        ranked_careers.sort(key=lambda x: x['match_score'], reverse=True)
        return ranked_careers[:limit]

    def get_job_recommendations(self, profile, jobs, limit=5):
        """
        Recommends jobs based on profile details and resume (skills, experience).
        """
        if not jobs:
            return []
            
        # Build user vector context
        user_skills = ", ".join(profile.get('current_skills', []))
        query = f"{profile.get('qualification', '')} {profile.get('stream', '')} {user_skills} {profile.get('target_goal', '')}"
        
        job_docs = []
        for job in jobs:
            job_skills = ", ".join(job.get('skills_required', []))
            doc = f"{job.get('title', '')} {job.get('company', '')} {job.get('description', '')} {job_skills} {job.get('location', '')} {job.get('type', '')}"
            job_docs.append(doc)
            
        if self.has_sklearn:
            try:
                if self.vectorizer is not None:
                    query_vec = self.vectorizer.transform([query.lower()])
                    job_vecs = self.vectorizer.transform(job_docs)
                    similarities = cosine_similarity(query_vec, job_vecs).flatten()
                else:
                    vectorizer = TfidfVectorizer(stop_words='english')
                    tfidf_matrix = vectorizer.fit_transform([query] + job_docs)
                    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            except Exception as e:
                print(f"[Recommender] Sklearn job matching failed: {e}. Falling back to pure Python.")
                similarities = self._pure_python_tfidf_cosine_similarity(query, job_docs)
        else:
            similarities = self._pure_python_tfidf_cosine_similarity(query, job_docs)
            
        ranked_jobs = []
        for idx, score in enumerate(similarities):
            # Calculate skills overlapping percentage
            user_skill_set = set(s.lower().strip() for s in profile.get('current_skills', []))
            job_skill_set = set(s.lower().strip() for s in jobs[idx].get('skills_required', []))
            
            overlap_bonus = 1.0
            if job_skill_set:
                intersect = user_skill_set.intersection(job_skill_set)
                overlap_ratio = len(intersect) / len(job_skill_set)
                overlap_bonus += (overlap_ratio * 0.5) # Up to 50% bonus for direct skill overlap
                
            # Filter by experience
            exp_mult = 1.0
            user_exp_val = profile.get('experience_years')
            user_exp = float(user_exp_val) if user_exp_val is not None else 0.0
            job_exp = float(jobs[idx].get('experience_required', 0.0))
            if user_exp < job_exp:
                # Penalty if candidate doesn't meet minimum experience requirement
                exp_mult = 0.7
                
            final_score = round(float(score) * overlap_bonus * exp_mult * 100, 1)
            final_score = min(final_score, 100.0)
            
            job_entry = jobs[idx].copy()
            job_entry['match_score'] = final_score
            ranked_jobs.append(job_entry)
            
        # Filter job recommendations by stream compatibility
        p_stream = profile.get('stream', '').strip()
        if p_stream:
            from models import Career
            try:
                db_careers = [c.to_dict() for c in Career.query.all()]
            except Exception:
                db_careers = []
            
            if db_careers:
                compatible_jobs = []
                for j in ranked_jobs:
                    if is_job_compatible_with_stream(j, p_stream, db_careers, self):
                        compatible_jobs.append(j)
                ranked_jobs = compatible_jobs

        ranked_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        return ranked_jobs[:limit]
