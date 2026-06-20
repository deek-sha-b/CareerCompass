class SkillAnalyzer:
    def __init__(self):
        pass

    def analyze_gap(self, user_skills, required_skills, courses_db):
        """
        Calculates skill gap percentage, missing skills, online course matches, and roadmap.
        
        user_skills: list of strings (e.g. ['python', 'html'])
        required_skills: list of strings (e.g. ['python', 'sql', 'docker', 'machine learning'])
        courses_db: list of Course dicts/objects to match against missing skills
        """
        user_skills_clean = [s.strip().lower() for s in user_skills if s.strip()]
        req_skills_clean = [s.strip().lower() for s in required_skills if s.strip()]
        
        if not req_skills_clean:
            return {
                'match_percentage': 100,
                'matching_skills': [],
                'missing_skills': [],
                'recommended_courses': [],
                'learning_roadmap': []
            }
            
        user_set = set(user_skills_clean)
        req_set = set(req_skills_clean)
        
        matching = list(user_set.intersection(req_set))
        missing = list(req_set.difference(user_set))
        
        # Calculate percentage match
        match_percentage = round((len(matching) / len(req_set)) * 100)
        
        # Find course recommendations for missing skills
        recommended_courses = []
        for missing_skill in missing:
            # Look for courses that list the missing skill in title or category
            skill_courses = []
            for course in courses_db:
                # Handle dictionary or DB object
                course_title = course.get('title', '').lower()
                course_cat = course.get('skill_category', '').lower()
                
                if (missing_skill in course_title or missing_skill in course_cat or 
                    course_cat in missing_skill or course_title in missing_skill):
                    skill_courses.append(course)
            
            # Sort courses by rating and select top 1-2 for this skill
            skill_courses.sort(key=lambda x: x.get('rating', 4.5), reverse=True)
            if skill_courses:
                recommended_courses.extend(skill_courses[:2])
                
        # Deduplicate courses by id
        seen_ids = set()
        unique_courses = []
        for c in recommended_courses:
            c_id = c.get('id')
            if c_id not in seen_ids:
                seen_ids.add(c_id)
                unique_courses.append(c)
                
        # Generate learning roadmap phases
        learning_roadmap = []
        
        if missing:
            # Phase 1: Foundation (first half of missing skills)
            phase1_skills = missing[:max(1, len(missing)//2)]
            phase1_courses = [c for c in unique_courses if any(s in c.get('title', '').lower() or s in c.get('skill_category', '').lower() for s in phase1_skills)]
            
            learning_roadmap.append({
                'phase': 1,
                'title': 'Phase 1: Foundation Building',
                'description': 'Master the core foundational concepts and tools required for this role.',
                'focus_skills': [s.title() for s in phase1_skills],
                'estimated_duration': f"{max(2, len(phase1_skills)*3)} weeks",
                'suggested_actions': [
                    f"Enroll in courses focusing on: {', '.join(s.title() for s in phase1_skills)}",
                    "Complete basic coding tutorials or concept review sessions",
                    "Build small, simple scripts/exercises utilizing these concepts"
                ]
            })
            
            # Phase 2: Core Development & Integration (second half of missing skills)
            phase2_skills = missing[max(1, len(missing)//2):]
            if phase2_skills:
                learning_roadmap.append({
                    'phase': 2,
                    'title': 'Phase 2: Specialized Knowledge & Tooling',
                    'description': 'Bridge intermediate tools and specialized libraries essential to professional practice.',
                    'focus_skills': [s.title() for s in phase2_skills],
                    'estimated_duration': f"{max(3, len(phase2_skills)*4)} weeks",
                    'suggested_actions': [
                        f"Dive deep into: {', '.join(s.title() for s in phase2_skills)}",
                        "Work on multi-module practice projects",
                        "Review code architecture and system-level interactions"
                    ]
                })
                
            # Phase 3: Portfolio & Job Readiness (Always present to guide application)
            learning_roadmap.append({
                'phase': len(learning_roadmap) + 1,
                'title': 'Phase 3: Portfolio Development & Mock Testing',
                'description': 'Apply your expanded skillset by building representative portfolio projects and undergoing interview preparation.',
                'focus_skills': ['Portfolio Projects', 'ATS Resume Review', 'Interview Prep'],
                'estimated_duration': '4 weeks',
                'suggested_actions': [
                    "Synthesize your new skills into 2 significant capstone projects and add them to Github/Portfolio",
                    "Run your resume through the ATS Resume Builder to check for keyword optimization",
                    "Conduct mock interview practice to polish soft/technical communication"
                ]
            })
        else:
            # If 100% skill match
            learning_roadmap.append({
                'phase': 1,
                'title': 'Phase 1: Skill Consolidation',
                'description': 'You already meet the skill requirements. Keep your skills updated and fresh.',
                'focus_skills': ['Advanced Applications', 'System Architecture'],
                'estimated_duration': '2 weeks',
                'suggested_actions': [
                    "Contribute to open-source projects using your skills",
                    "Review advanced system designs and best practices in the field"
                ]
            })
            learning_roadmap.append({
                'phase': 2,
                'title': 'Phase 2: Resume & Interview Prep',
                'description': 'Directly prepare for applications.',
                'focus_skills': ['ATS Optimization', 'Interview Practice'],
                'estimated_duration': '3 weeks',
                'suggested_actions': [
                    "Optimize your resume for specific companies",
                    "Practice mock interviews and review common interview questions"
                ]
            })
            
        return {
            'match_percentage': match_percentage,
            'matching_skills': [s.title() for s in matching],
            'missing_skills': [s.title() for s in missing],
            'recommended_courses': unique_courses[:4], # Top 4 course recommendations
            'learning_roadmap': learning_roadmap
        }
