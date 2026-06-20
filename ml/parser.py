import re

ACTION_VERBS = [
    'achieved', 'analyzed', 'built', 'created', 'coordinated', 'designed', 'developed',
    'established', 'executed', 'formulated', 'implemented', 'improved', 'increased',
    'initiated', 'introduced', 'led', 'managed', 'maximized', 'minimized', 'negotiated',
    'organized', 'optimized', 'pioneered', 'planned', 'produced', 'restructured',
    'spearheaded', 'solved', 'trained', 'transformed'
]

class ResumeParser:
    def __init__(self):
        pass

    def calculate_ats_score(self, resume_data, target_skills=None):
        """
        Parses resume elements to compute an ATS score out of 100 and suggestions.
        
        resume_data: dictionary containing resume fields (name, email, phone, location, summary, 
                     education, skills, experience, projects, certifications, achievements)
        target_skills: list of required skills for target career
        """
        score = 0
        suggestions = []
        missing_skills_suggested = []
        
        # 1. Contact Information Completeness (Max 15 points)
        contact_points = 0
        if resume_data.get('name'):
            contact_points += 5
        else:
            suggestions.append("Candidate name is missing. Ensure your name is clearly visible at the top.")
            
        if resume_data.get('email'):
            contact_points += 5
        else:
            suggestions.append("Email address is missing. Recruiter contact channels are critical.")
            
        if resume_data.get('phone'):
            contact_points += 5
        else:
            suggestions.append("Phone number is missing. Recruiters prefer immediate callback lines.")
            
        score += contact_points

        # 2. Executive Summary Quality (Max 15 points)
        summary = resume_data.get('summary', '').strip()
        if not summary:
            suggestions.append("Professional Summary is missing. Add a 3-4 sentence elevator pitch highlights.")
        else:
            word_count = len(summary.split())
            if word_count < 15:
                score += 5
                suggestions.append("Your Professional Summary is too brief. Elaborate on your target direction and core strengths.")
            elif word_count > 120:
                score += 8
                suggestions.append("Your Professional Summary is too wordy. Condense it to under 100 words for recruiter scannability.")
            else:
                score += 15 # Perfect length

        # 3. Work Experience Completeness & Action Verbs (Max 25 points)
        exp_list = resume_data.get('experience', [])
        if not exp_list:
            # Check if student (they might have projects instead)
            suggestions.append("No Work Experience listed. If you're a student, list Internships, Volunteer positions, or Freelance projects.")
        else:
            score += 15 # Section present
            
            # Check for action verbs and descriptions
            found_verbs = 0
            has_metrics = False
            for job in exp_list:
                desc = job.get('description', '').lower()
                for verb in ACTION_VERBS:
                    if re.search(r'\b' + verb + r'\w*\b', desc):
                        found_verbs += 1
                # Check for metrics (numbers like 10%, $5k, 500+ users)
                if re.search(r'\b\d+%|\b\$\d+|\b\d+\s+users|\b\d+\s+clients', desc):
                    has_metrics = True
            
            if found_verbs >= 3:
                score += 5
            else:
                suggestions.append("Incorporate more action-oriented verbs (e.g., 'Spearheaded', 'Optimized', 'Executed') in your job descriptions.")
                
            if has_metrics:
                score += 5
            else:
                suggestions.append("Quantify your achievements! Use numbers (percentages, revenue, team sizes) to show the scale of your impact.")

        # 4. Project Experience (Max 15 points)
        proj_list = resume_data.get('projects', [])
        if not proj_list:
            suggestions.append("Projects section is missing. Projects are vital to showcase hands-on application of skills.")
        else:
            score += 15

        # 5. Education History (Max 10 points)
        edu_list = resume_data.get('education', [])
        if not edu_list:
            suggestions.append("Education details are missing. Add your university degree, college, or school history.")
        else:
            score += 10

        # 6. Skill Keywords Alignment (Max 20 points)
        user_skills = [s.strip().lower() for s in resume_data.get('skills', []) if s.strip()]
        
        if not user_skills:
            suggestions.append("Skills section is empty! Recruiters search resumes using skill keywords.")
        else:
            if target_skills:
                # Align with target job requirements
                target_skills_clean = [ts.strip().lower() for ts in target_skills if ts.strip()]
                user_set = set(user_skills)
                target_set = set(target_skills_clean)
                
                matched_set = user_set.intersection(target_set)
                missing_set = target_set.difference(user_set)
                
                # Score based on keyword coverage percentage
                if target_skills_clean:
                    coverage = len(matched_set) / len(target_skills_clean)
                    score += round(coverage * 20)
                    
                    if missing_set:
                        missing_skills_suggested = [s.title() for s in missing_set]
                        suggestions.append(f"Missing target keywords! To optimize for ATS, try incorporating: {', '.join(missing_skills_suggested[:4])}")
                else:
                    score += 15 # Standard score if target skills list is empty
            else:
                # Default score if no target skills to compare
                score += min(len(user_skills) * 2, 20)
                if len(user_skills) < 6:
                    suggestions.append("Add more skills to your resume. Target a minimum of 8-10 technical and professional keywords.")

        # Cap score at 100
        score = min(max(score, 0), 100)
        
        return {
            'ats_score': score,
            'suggestions': suggestions if suggestions else ["Outstanding! Your resume is highly structured, quantifiable, and optimized for ATS systems."],
            'missing_skills': missing_skills_suggested
        }
