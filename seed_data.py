from app import app
from models import db, User, Profile, Career, Job, Course
import json

def seed_database():
    print("Seeding database...")
    
    # 1. Add Default Admin & Student Accounts
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@careerguide.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        admin_prof = Profile(user_id=admin.id, full_name="System Administrator")
        db.session.add(admin_prof)
        
    if not User.query.filter_by(username='student').first():
        student = User(username='student', email='student@careerguide.com', role='student')
        student.set_password('student123')
        db.session.add(student)
        db.session.flush()
        student_prof = Profile(
            user_id=student.id, 
            full_name="Student Candidate",
            stream="Science/Computer Applications",
            qualification="Undergraduate",
            current_skills="Python, SQL, Git",
            interests="Coding, Solving Puzzles"
        )
        db.session.add(student_prof)

    # 2. Add Careers (supporting all streams/degrees)
    # We define robust roadmap structures for each career
    careers_data = [
        {
            'title': 'Software Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design, develop, and test software applications. Solve complex programming challenges and build scalable systems.',
            'required_skills': 'Python, JavaScript, Data Structures, Algorithms, SQL, Git, Software Design',
            'min_education': 'Undergraduate (B.Tech/B.E/BCA/B.Sc CS)',
            'salary_range': '₹4,00,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in CS, MS in Computer Science, MBA',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Acquire Degree', 'desc': 'Complete a B.Tech, BCA, or B.Sc in Computer Science or related engineering field.'},
                {'step': 2, 'title': 'Master Coding Fundamentals', 'desc': 'Learn Python, Java, or JavaScript. Study Data Structures & Algorithms (DSA).'},
                {'step': 3, 'title': 'Build Portfolio Projects', 'desc': 'Build 3-4 web/mobile applications and host them publicly on GitHub.'},
                {'step': 4, 'title': 'Internship Placement', 'desc': 'Secure a 3-6 month software engineering internship to gain commercial experience.'},
                {'step': 5, 'title': 'Full-Time Job Search', 'desc': 'Target Junior Developer positions, practice coding assessments, and optimize your ATS resume.'}
            ])
        },
        {
            'title': 'Data Scientist',
            'stream': 'Science/Computer Applications',
            'description': 'Analyze complex data sets to extract insights, build predictive models, and design machine learning systems.',
            'required_skills': 'Python, R, Machine Learning, Statistics, SQL, Pandas, NumPy, Data Visualization',
            'min_education': 'Undergraduate (B.Sc CS/Math/Stats, BCA, B.Tech)',
            'salary_range': '₹6,00,000 - ₹24,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Sc in Data Science, Ph.D. in Machine Learning/Statistics',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Core Education', 'desc': 'Earn a Bachelor\'s degree in Computer Science, Math, Statistics, or Engineering.'},
                {'step': 2, 'title': 'Math & Coding Foundations', 'desc': 'Master Linear Algebra, Calculus, Probability, and Python programming.'},
                {'step': 3, 'title': 'Data Analysis & Wrangling', 'desc': 'Learn Pandas, SQL, and data visualization tools (Tableau/Matplotlib).'},
                {'step': 4, 'title': 'Machine Learning Methods', 'desc': 'Study supervised/unsupervised algorithms, evaluation metrics, and Deep Learning.'},
                {'step': 5, 'title': 'Capstone Portfolio', 'desc': 'Create end-to-end data analysis/prediction projects hosted on Kaggle or GitHub.'}
            ])
        },
        {
            'title': 'Chartered Accountant (CA)',
            'stream': 'Commerce/Management',
            'description': 'Manage financial accounts, conduct audits, offer tax advisory, and guide corporate financial strategies.',
            'required_skills': 'Taxation, Auditing, Corporate Law, Accounting Standards, Excel, Financial Analysis',
            'min_education': 'Undergraduate (B.Com/BBA) & ICAI Certification',
            'salary_range': '₹7,00,000 - ₹20,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'DISA, CFA (Chartered Financial Analyst), MBA Finance',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Register with ICAI', 'desc': 'Register for the CA Foundation exam after completing Higher Secondary.'},
                {'step': 2, 'title': 'Pass Intermediate Exam', 'desc': 'Complete the CA Intermediate course covering corporate and taxation laws.'},
                {'step': 3, 'title': 'Articleship Training', 'desc': 'Undergo 2-3 years of practical articleship training under a practicing CA.'},
                {'step': 4, 'title': 'CA Final Examination', 'desc': 'Prepare and pass the CA Final Exam covering advanced auditing and strategic finance.'},
                {'step': 5, 'title': 'Membership Enrollment', 'desc': 'Register as a member of the Institute of Chartered Accountants of India.'}
            ])
        },
        {
            'title': 'UX/UI Designer',
            'stream': 'Design/Arts',
            'description': 'Design user experiences and interfaces for websites, apps, and software. Conduct user research and wireframing.',
            'required_skills': 'Figma, Wireframing, User Research, Prototyping, Visual Communication, Color Theory',
            'min_education': 'Undergraduate (B.Des/BFA/Fine Arts/Humanities)',
            'salary_range': '₹4,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'M.Des, Interaction Design Certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Learn Figma & Design Basics', 'desc': 'Study color theory, layout composition, typography, and master Figma/Adobe XD.'},
                {'step': 2, 'title': 'Understand UX Research', 'desc': 'Learn user personas, user journeys, wireframing, and usability testing.'},
                {'step': 3, 'title': 'Redesign Projects', 'desc': 'Pick existing apps and create redesign case studies documenting your process.'},
                {'step': 4, 'title': 'Build UX Portfolio', 'desc': 'Publish your case studies on Behance, Dribbble, or a personal website.'},
                {'step': 5, 'title': 'Apply for Junior UX/UI Roles', 'desc': 'Apply for design internships and junior UI positions, focusing on process explanations.'}
            ])
        },
        {
            'title': 'Civil/Structural Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Plan, design, and supervise the construction of infrastructure projects such as roads, bridges, and buildings.',
            'required_skills': 'AutoCAD, Structural Analysis, Project Management, Concrete Design, Estimation, Site Supervision',
            'min_education': 'Undergraduate (B.Tech Civil / Diploma Civil)',
            'salary_range': '₹3,50,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Moderate',
            'higher_studies_options': 'M.Tech Structural Engineering, Construction Management',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Academic Degree', 'desc': 'Obtain a Bachelor\'s degree or Diploma in Civil Engineering.'},
                {'step': 2, 'title': 'Learn CAD Software', 'desc': 'Become proficient in AutoCAD, Revit, or STAAD.Pro for structural drafting.'},
                {'step': 3, 'title': 'Site Internships', 'desc': 'Work as an intern at construction sites to learn execution and supervision.'},
                {'step': 4, 'title': 'Learn Code Standards', 'desc': 'Study regional building codes and safety regulations.'},
                {'step': 5, 'title': 'Associate Engineer Role', 'desc': 'Join a construction firm or design agency as a junior engineer.'}
            ])
        },
        {
            'title': 'Pharmacist',
            'stream': 'Pharmacy/Medical',
            'description': 'Dispense medications, advise patients on drug safety, manage pharmacy stock, and consult with doctors on prescriptions.',
            'required_skills': 'Pharmacology, Drug Chemistry, Inventory Management, Customer Service, Drug Regulations',
            'min_education': 'Undergraduate (B.Pharm / D.Pharm)',
            'salary_range': '₹2,50,000 - ₹6,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'M.Pharm, Pharm.D, Clinical Research Certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Earn Pharmacy Qualification', 'desc': 'Complete a 2-year Diploma (D.Pharm) or 4-year Bachelor (B.Pharm) in Pharmacy.'},
                {'step': 2, 'title': 'State Council Registration', 'desc': 'Register as a Registered Pharmacist with your state\'s Pharmacy Council.'},
                {'step': 3, 'title': 'Clinical/Retail Training', 'desc': 'Undergo mandatory hospital or retail pharmacy internships.'},
                {'step': 4, 'title': 'Drug Storage Familiarization', 'desc': 'Learn inventory systems, drug interactions, and storage regulations.'},
                {'step': 5, 'title': 'Establish Practice', 'desc': 'Join a hospital pharmacy, retail chain, or start an independent drugstore.'}
            ])
        },
        {
            'title': 'Corporate Lawyer',
            'stream': 'Law',
            'description': 'Advise businesses on legal rights, duties, mergers and acquisitions, contract compliance, and represent corporations in court.',
            'required_skills': 'Contract Drafting, Corporate Law, Litigation, Legal Research, Negotiation, Dispute Resolution',
            'min_education': 'Undergraduate (LLB / BA-LLB)',
            'salary_range': '₹6,00,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'LLM in Corporate Law, Business Law certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Law Degree', 'desc': 'Complete a 5-year integrated law course (BA-LLB) or a 3-year LLB after graduation.'},
                {'step': 2, 'title': 'Bar Exam Clearance', 'desc': 'Pass the All India Bar Examination (AIBE) to get licensed for court practice.'},
                {'step': 3, 'title': 'Internships under Lawyers', 'desc': 'Intern at corporate law firms, legal departments, or senior advocates.'},
                {'step': 4, 'title': 'Master Legal Drafting', 'desc': 'Develop expertise in drafting business contracts, NDAs, and corporate policies.'},
                {'step': 5, 'title': 'Associate in Law Firm', 'desc': 'Join a corporate law firm as a Junior Associate.'}
            ])
        },
        {
            'title': 'Agricultural Consultant',
            'stream': 'Agriculture/Science',
            'description': 'Consult farms and businesses on soil quality, crop rotations, water management, pest control, and food safety policies.',
            'required_skills': 'Agronomy, Soil Science, Pest Management, Irrigation Systems, Sustainable Agriculture',
            'min_education': 'Undergraduate (B.Sc Agriculture / B.Sc Botany)',
            'salary_range': '₹3,00,000 - ₹7,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Sc Agriculture, Agronomy specialized programs',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Agriculture Education', 'desc': 'Earn a Bachelor of Science (B.Sc) in Agriculture.'},
                {'step': 2, 'title': 'Field Internships', 'desc': 'Work with agricultural research stations or crop science firms.'},
                {'step': 3, 'title': 'Learn Modern Farming Tech', 'desc': 'Gain skills in hydroponics, organic farming, and precision soil sensors.'},
                {'step': 4, 'title': 'Environmental Regulations', 'desc': 'Understand organic certification guidelines and environmental policies.'},
                {'step': 5, 'title': 'Consultant Practice', 'desc': 'Join farm consultancies, fertilizer firms, or start independent consulting.'}
            ])
        },
        {
            'title': 'Secondary School Teacher',
            'stream': 'Education/Humanities',
            'description': 'Plan lessons, manage classrooms, instruct students in academic courses, and assess student development and grading.',
            'required_skills': 'Classroom Management, Lesson Planning, Subject Expertise, Communication, Student Evaluation',
            'min_education': 'Undergraduate & B.Ed (Bachelor of Education)',
            'salary_range': '₹3,00,000 - ₹6,50,000',
            'type': 'Government Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Ed, MA in Subject Field, Ph.D. in Education',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Undergraduate degree', 'desc': 'Obtain a Bachelor\'s degree in Arts, Commerce, or Science in your teaching subject.'},
                {'step': 2, 'title': 'Professional B.Ed', 'desc': 'Complete a 2-year Bachelor of Education (B.Ed) degree.'},
                {'step': 3, 'title': 'Teacher Eligibility Test', 'desc': 'Pass national/state eligibility tests like CTET or TET.'},
                {'step': 4, 'title': 'Student Teaching Practice', 'desc': 'Undergo classroom training at local schools during your B.Ed program.'},
                {'step': 5, 'title': 'School Application', 'desc': 'Apply to private and government schools, showcasing classroom design portfolios.'}
            ])
        },
        {
            'title': 'Hotel Manager',
            'stream': 'Hotel Management/Vocational',
            'description': 'Supervise daily operations of a hotel or resort, including front desk, housekeeping, catering, budgets, and staff.',
            'required_skills': 'Hospitality Management, Customer Relations, Operations, Budgeting, Staff Management',
            'min_education': 'Undergraduate (BHM / B.Sc Hospitality)',
            'salary_range': '₹4,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'MBA in Hospitality, Specialized culinary certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Hotel Management Degree', 'desc': 'Obtain a Bachelor of Hotel Management (BHM) or related degree.'},
                {'step': 2, 'title': 'Department Rotations', 'desc': 'Perform trainee internships across front-desk, kitchen, and housekeeping departments.'},
                {'step': 3, 'title': 'Supervisor Role', 'desc': 'Graduate into supervisor or assistant roles in high-tier restaurant or hotels.'},
                {'step': 4, 'title': 'Financial Management', 'desc': 'Learn budget allocation, marketing strategies, and procurement systems.'},
                {'step': 5, 'title': 'General Manager', 'desc': 'Apply for General Hotel Manager positions with a history of operational savings.'}
            ])
        },
        {
            'title': 'Cloud Architect',
            'stream': 'Engineering/Technology',
            'description': 'Design and implement enterprise cloud strategy, manage cloud migrations, and maintain high-availability cloud infrastructure.',
            'required_skills': 'Cloud Computing, AWS, Azure, Kubernetes, Docker, DevOps, Systems Design',
            'min_education': 'Undergraduate (B.Tech/B.E/BCA/B.Sc CS)',
            'salary_range': '₹6,00,000 - ₹22,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in Cloud Computing, AWS Certified Solutions Architect, MBA',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Acquire Core CS Degree', 'desc': 'Complete a B.Tech, BCA, or B.Sc in Computer Science.'},
                {'step': 2, 'title': 'Learn Linux & Networking', 'desc': 'Master terminal operations, subnetting, TCP/IP, and shell scripting.'},
                {'step': 3, 'title': 'Master Containerization', 'desc': 'Learn Docker and Kubernetes orchestration.'},
                {'step': 4, 'title': 'Cloud Certification', 'desc': 'Obtain AWS Solutions Architect or Google Professional Cloud Architect credentials.'},
                {'step': 5, 'title': 'System Design Practice', 'desc': 'Design and host multi-tier distributed architectures on cloud platforms.'}
            ])
        },
        {
            'title': 'Digital Marketer',
            'stream': 'Commerce/Management',
            'description': 'Plan and execute online advertising campaigns, optimize search engine presence, and manage social media branding campaigns.',
            'required_skills': 'SEO, SEM, Google Analytics, Content Writing, Social Media Marketing, Copywriting, Email Campaigns',
            'min_education': 'Undergraduate (BBA/B.Com/B.A)',
            'salary_range': '₹3,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'MBA in Marketing, Google Analytics Academy, HubSpot Academy certs',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Learn Marketing Principles', 'desc': 'Study consumer psychology, brand placement, and online marketing channels.'},
                {'step': 2, 'title': 'Get Google & HubSpot Certified', 'desc': 'Complete free online certifications on SEO, SEM, Google Ads, and inbound marketing.'},
                {'step': 3, 'title': 'Run A Web Project', 'desc': 'Create a blog or website and apply SEO principles to grow its traffic.'},
                {'step': 4, 'title': 'Learn Analytics', 'desc': 'Master Google Analytics to understand traffic attribution and conversion loops.'},
                {'step': 5, 'title': 'Digital Associate', 'desc': 'Join a marketing agency as a junior analyst or media buyer.'}
            ])
        },
        {
            'title': 'Graphic Designer',
            'stream': 'Design/Arts',
            'description': 'Create visual concepts, advertising layouts, product mockups, and corporate brand identities using graphic tools.',
            'required_skills': 'Photoshop, Illustrator, InDesign, Typography, Branding, Visual Design, Creativity',
            'min_education': 'Undergraduate (B.Des/BFA/Diploma)',
            'salary_range': '₹2,50,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Des, Specialized courses in Typography or Motion Graphics',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Learn Core Design Principles', 'desc': 'Understand composition, grid systems, alignment, color harmony, and typography.'},
                {'step': 2, 'title': 'Master Vector & Raster Tools', 'desc': 'Learn Adobe Illustrator for vector work and Photoshop for image editing.'},
                {'step': 3, 'title': 'Create Design Briefs', 'desc': 'Create mock redesign projects for logos, flyers, book covers, and social media posts.'},
                {'step': 4, 'title': 'Publish Design Portfolio', 'desc': 'Curate your best 6-8 designs on Behance or Dribbble.'},
                {'step': 5, 'title': 'Freelance or Junior Artist', 'desc': 'Apply for Junior Graphic Designer roles or take up freelance gigs to gain client experience.'}
            ])
        },
        {
            'title': 'Product Manager',
            'stream': 'Commerce/Management',
            'description': 'Define product visions and roadmaps, manage the development lifecycle, and coordinate engineering and marketing teams.',
            'required_skills': 'Agile, Product Strategy, User Research, Jira, Product Analytics, Roadmapping, Communications',
            'min_education': 'Undergraduate + MBA preferred',
            'salary_range': '₹8,00,000 - ₹26,0,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Product Management Professional (PMP), Agile certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Build Domain Knowledge', 'desc': 'Understand basic software architecture, marketing, and business KPIs.'},
                {'step': 2, 'title': 'Work in Tech or Business', 'desc': 'Gain initial experience in software development, business analysis, or sales.'},
                {'step': 3, 'title': 'Master Product Toolkits', 'desc': 'Learn Jira, Confluence, Amplitude/Mixpanel, and user journey mapping.'},
                {'step': 4, 'title': 'Transition or MBA', 'desc': 'Pursue an MBA or attempt internal transition into Associate PM role at your company.'},
                {'step': 5, 'title': 'Product Management Lead', 'desc': 'Own a specific product domain, managing backlog and engineering execution.'}
            ])
        },
        {
            'title': 'Financial Analyst',
            'stream': 'Commerce/Management',
            'description': 'Perform financial modeling, evaluate investment opportunities, analyze balance sheets, and assess market risks.',
            'required_skills': 'Financial Modeling, Excel, Valuation, Accounting, Python, Quantitative Reasoning, Finance Standards',
            'min_education': 'Undergraduate (B.Com/BBA/B.Sc Finance)',
            'salary_range': '₹4,00,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'CFA (Chartered Financial Analyst), MBA Finance, FRM',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Finance Core Education', 'desc': 'Earn a Bachelor\'s degree in Commerce, Finance, or Economics.'},
                {'step': 2, 'title': 'Advanced Excel Modeling', 'desc': 'Master complex formulas, lookup tables, and dynamic cash flow forecasts in Excel.'},
                {'step': 3, 'title': 'Study Corporate Accounts', 'desc': 'Learn to read balance sheets, P&L accounts, and calculate valuation ratios.'},
                {'step': 4, 'title': 'Enroll in CFA Program', 'desc': 'Prepare and clear the CFA Level 1 exam to gain global credibility.'},
                {'step': 5, 'title': 'Investment Analyst Role', 'desc': 'Apply to equity research firms, commercial banks, or brokerage houses.'}
            ])
        },
        {
            'title': 'HR Specialist',
            'stream': 'Commerce/Management',
            'description': 'Manage employee recruitment, coordinate onboarding, design workplace policies, and coordinate conflict resolution.',
            'required_skills': 'Recruiting, Interpersonal Skills, HR Policies, Conflict Resolution, Negotiation, Compliance',
            'min_education': 'Undergraduate (BBA/B.Com/B.A)',
            'salary_range': '₹3,00,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Stable',
            'higher_studies_options': 'MBA in HR, Professional in Human Resources (PHR) certification',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Acquire Degree', 'desc': 'Earn a Bachelor\'s degree in Business, Psychology, or Humanities.'},
                {'step': 2, 'title': 'Sourcing & Screening Practice', 'desc': 'Learn to search candidate resumes on LinkedIn, Naukri, and screening templates.'},
                {'step': 3, 'title': 'Understand Labor Laws', 'desc': 'Study local labor regulations, employee insurance systems, and tax filings.'},
                {'step': 4, 'title': 'HR Internship', 'desc': 'Work as an HR intern to get experience with recruiting loops and documentation.'},
                {'step': 5, 'title': 'HR Associate', 'desc': 'Join corporate HR teams managing talent acquisition or employee engagement.'}
            ])
        },
        {
            'title': 'Doctor',
            'stream': 'Medical/Pharmacy',
            'description': 'Diagnose patient medical conditions, prescribe pharmaceutical medications, run medical procedures, and supervise treatments.',
            'required_skills': 'Clinical Medicine, Surgery, Patient Diagnosis, Patient Care, Healthcare Regulations, Pharmacology',
            'min_education': 'Undergraduate (MBBS / MD)',
            'salary_range': '₹8,0,000 - ₹30,0,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'MD, MS, Fellowship certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Clear NEET Exam', 'desc': 'Prepare and score high marks in pre-medical entrance exams (NEET).'},
                {'step': 2, 'title': 'MBBS Residency', 'desc': 'Complete the 5.5-year Bachelor of Medicine and Bachelor of Surgery program.'},
                {'step': 3, 'title': 'Compulsory Internship', 'desc': 'Complete 1 year of mandatory rotation internships at local hospitals.'},
                {'step': 4, 'title': 'Medical Council License', 'desc': 'Register as a licensed medical practitioner with the Medical Council.'},
                {'step': 5, 'title': 'Post-Graduation MD/MS', 'desc': 'Clear NEET PG and choose clinical specialization (Pediatrics, Surgery, etc.).'}
            ])
        },
        {
            'title': 'Mechanical Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design mechanical tools, troubleshoot heat exchanger designs, run plant machinery operations, and supervise manufacturing.',
            'required_skills': 'CAD, SolidWorks, Thermodynamics, Fluid Mechanics, Manufacturing Processes, Materials Science',
            'min_education': 'Undergraduate (B.Tech Mechanical / Diploma Mechanical)',
            'salary_range': '₹3,50,000 - ₹11,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Moderate',
            'higher_studies_options': 'M.Tech in Thermal Engineering, MS in Robotics, MBA',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Engineering degree', 'desc': 'Earn a Bachelor of Technology (B.Tech) in Mechanical Engineering.'},
                {'step': 2, 'title': 'Master CAD Modelling', 'desc': 'Learn Autodesk AutoCAD, SolidWorks, or CATIA for 3D modeling.'},
                {'step': 3, 'title': 'Factory Internships', 'desc': 'Intern at assembly lines, steel plants, or automotive workshops.'},
                {'step': 4, 'title': 'Learn Testing Tools', 'desc': 'Master finite element analysis (FEA) and computational fluid dynamics (CFD).'},
                {'step': 5, 'title': 'Design/Quality Engineer', 'desc': 'Apply for design engineer, operations engineer, or quality control specialist.'}
            ])
        },
        {
            'title': 'Content Writer',
            'stream': 'Humanities/Arts',
            'description': 'Write engaging article text, blog posts, marketing copies, and digital web content for brands and publications.',
            'required_skills': 'Content Writing, Copywriting, SEO, Research, Editing, Blogging, Creative Writing',
            'min_education': 'Undergraduate (B.A. English/Humanities/Journalism)',
            'salary_range': '₹2,50,000 - ₹7,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.A. in English, Journalism, Creative Writing certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Obtain Degree', 'desc': 'Complete a Bachelor\'s degree in English, Journalism, or a related Humanities field.'},
                {'step': 2, 'title': 'Build Writing Portfolio', 'desc': 'Create a personal blog or write free guest posts to showcase your style and versatility.'},
                {'step': 3, 'title': 'Learn SEO Basics', 'desc': 'Master keyword research, search intent, and search engine optimization concepts.'},
                {'step': 4, 'title': 'Freelancing', 'desc': 'Start taking writing gigs on platforms like Upwork or Fiverr to build client reviews.'},
                {'step': 5, 'title': 'Full-Time Copywriting', 'desc': 'Apply to marketing agencies, media houses, or tech firms as a staff content writer.'}
            ])
        },
        {
            'title': 'Clinical Psychologist',
            'stream': 'Humanities/Arts',
            'description': 'Diagnose and treat mental, emotional, and behavioral disorders. Conduct counseling sessions and clinical assessments.',
            'required_skills': 'Clinical Psychology, Counseling, Patient Care, Active Listening, Emotional Intelligence, Mental Health Regulations',
            'min_education': 'Postgraduate (M.A./M.Sc Psychology) & M.Phil',
            'salary_range': '₹4,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Ph.D. in Clinical Psychology, Psy.D.',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Bachelor\'s Degree', 'desc': 'Complete a Bachelor of Arts or Science (B.A./B.Sc.) in Psychology.'},
                {'step': 2, 'title': 'Master\'s Degree', 'desc': 'Pursue a Master of Arts or Science (M.A./M.Sc.) in Clinical Psychology.'},
                {'step': 3, 'title': 'M.Phil / License Course', 'desc': 'Obtain a 2-year M.Phil in Clinical Psychology from an RCI-recognized institute.'},
                {'step': 4, 'title': 'Supervised Clinical Training', 'desc': 'Complete a clinical internship/residency under a licensed psychiatrist/psychologist.'},
                {'step': 5, 'title': 'Register & Practice', 'desc': 'Register with the Rehabilitation Council of India (RCI) and start private practice or join a clinic.'}
            ])
        },
        {
            'title': 'Chef / Culinary Artist',
            'stream': 'Hotel Management/Vocational',
            'description': 'Plan menus, prepare high-quality culinary dishes, supervise kitchen staff, and oversee food safety in commercial kitchens.',
            'required_skills': 'Culinary Arts, Menu Planning, Kitchen Operations, Food Safety, Recipe Development, Plating',
            'min_education': 'Undergraduate (BHM / Diploma in Culinary Arts)',
            'salary_range': '₹3,00,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'Advanced Culinary Arts Diplomas, MBA in Hospitality',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Culinary Training', 'desc': 'Earn a Diploma or Bachelor\'s in Hotel Management specializing in Food Production/Culinary Arts.'},
                {'step': 2, 'title': 'Kitchen Entry', 'desc': 'Start as a Commis Chef (Junior Cook) in a professional kitchen, learning food prep and hygiene.'},
                {'step': 3, 'title': 'Section Lead', 'desc': 'Graduate to a Chef de Partie, running a specific kitchen section (sauces, grilling, etc.).'},
                {'step': 4, 'title': 'Sous Chef Role', 'desc': 'Become a Sous Chef, acting as second-in-command, managing kitchen staff and ordering stock.'},
                {'step': 5, 'title': 'Executive Chef', 'desc': 'Take full charge of menu creation, budgeting, and kitchen operations as an Executive Chef.'}
            ])
        },
        {
            'title': 'Industrial Electrician',
            'stream': 'Hotel Management/Vocational',
            'description': 'Install, maintain, and repair electrical systems, heavy machinery, controls, and wiring in industrial settings.',
            'required_skills': 'Electrical Wiring, Troubleshooting, PLC Systems, Blueprint Reading, Safety Standards, Industrial Equipment',
            'min_education': 'ITI Certification / Diploma in Electrical Engineering',
            'salary_range': '₹2,00,000 - ₹5,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'B.Tech in Electrical Engineering, Safety Certifications',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Vocational Training', 'desc': 'Complete ITI (Industrial Training Institute) course or Diploma in Electrical Engineering.'},
                {'step': 2, 'title': 'Apprenticeship', 'desc': 'Secure a 1-2 year industrial apprenticeship under a licensed supervisor.'},
                {'step': 3, 'title': 'Electrician License', 'desc': 'Pass the state electrical licensing board exams to become a certified electrical technician.'},
                {'step': 4, 'title': 'Industrial Maintenance', 'desc': 'Work in factories or manufacturing units, focusing on PLC control cabinets and power circuits.'},
                {'step': 5, 'title': 'Senior Electrician / Foreman', 'desc': 'Advance to a foreman or maintenance manager role overseeing industrial grid maintenance.'}
            ])
        },
        {
            'title': 'Database Administrator',
            'stream': 'Science/Computer Applications',
            'description': 'Configure, manage, monitor, and optimize database management systems (DBMS) to ensure high-performance, security, and data integrity.',
            'required_skills': 'SQL, Database Administration, Backup & Recovery, Performance Tuning, Security Compliance, Oracle, PostgreSQL',
            'min_education': 'Undergraduate (BCA/B.Sc CS/B.Tech)',
            'salary_range': '₹5,00,000 - ₹14,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc Computer Science, Database Professional Certifications (Oracle, MS SQL)',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Core Education', 'desc': 'Complete a BCA, B.Sc in Computer Science, or B.Tech degree.'},
                {'step': 2, 'title': 'SQL Mastery', "desc": "Master complex queries, indexing, schemas, triggers, and query execution plans."},
                {'step': 3, 'title': 'Learn DB Platforms', 'desc': 'Get familiar with MySQL, PostgreSQL, Oracle, and MS SQL Server administrations.'},
                {'step': 4, 'title': 'Certifications', 'desc': 'Obtain administrative certifications like Oracle Certified Associate or AWS Database Specialist.'},
                {'step': 5, 'title': 'Junior DBA Role', 'desc': 'Apply for Junior DBA positions, concentrating on backups, recoveries, and user access management.'}
            ])
        },
        {
            'title': 'Cybersecurity Analyst',
            'stream': 'Engineering/Technology',
            'description': 'Protect organization networks, firewalls, and data assets from cyber threats, malware, hacking attacks, and security vulnerabilities.',
            'required_skills': 'Network Security, Penetration Testing, Threat Intelligence, Firewalls, Linux, Cryptography, Incident Response',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹5,00,000 - ₹16,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in Information Security, CISSP, CEH (Certified Ethical Hacker)',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Acquire CS Degree', 'desc': 'Earn a B.Tech, BCA, or B.Sc in Computer Science or IT.'},
                {'step': 2, 'title': 'Networking & OS Fundamentals', 'desc': 'Master TCP/IP, Linux command line, scripting (Bash/Python), and active directory concepts.'},
                {'step': 3, 'title': 'Cyber Security Certs', 'desc': 'Study and pass CompTIA Security+, CEH (Ethical Hacking), or OSCP.'},
                {'step': 4, 'title': 'Hands-On Laboratories', 'desc': 'Practice CTFs (Capture The Flag) on platforms like TryHackMe or HackTheBox to learn exploit analysis.'},
                {'step': 5, 'title': 'Security Analyst Placement', 'desc': 'Secure a position in a SOC (Security Operations Center) monitoring systems and responding to alerts.'}
            ])
        },
        {
            'title': 'Fashion Designer',
            'stream': 'Design/Arts',
            'description': 'Sketch fashion designs, select textile fabrics, create custom clothing apparel and accessories, and present runway lines.',
            'required_skills': 'Fashion Design, Sketching, Textile Selection, Pattern Making, Sewing, Trend Analysis, Creativity',
            'min_education': 'Undergraduate (B.Des Fashion / Diploma in Fashion Tech)',
            'salary_range': '₹2,50,000 - ₹9,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Des, Specialized courses in haute couture or luxury brand management',
            'roadmap_steps': json.dumps([
                {'step': 1, 'title': 'Fashion Education', 'desc': 'Earn a Bachelor of Design (B.Des) in Fashion Design or a related vocational diploma.'},
                {'step': 2, 'title': 'Master Designing Tools', 'desc': 'Learn manual sketching, pattern making, sewing techniques, and digital CAD tools (CLO 3D).'},
                {'step': 3, 'title': 'Apparel Industry Internship', 'desc': 'Intern at fashion design houses, garment manufacturing units, or retail brands.'},
                {'step': 4, 'title': 'Develop Portfolio', 'desc': 'Create a design portfolio showcasing high-quality photos of your constructed garments and sketches.'},
                {'step': 5, 'title': 'Launch Brand / Design Role', 'desc': 'Join a apparel brand as an assistant designer, or launch your boutique/independent label.'}
            ])
        },
        {
            'title': 'Machine Learning Engineer',
            'stream': 'Science/Computer Applications',
            'description': 'Design, build, and deploy machine learning models and artificial intelligence systems to solve complex business problems.',
            'required_skills': 'Python, Machine Learning, Deep Learning, SQL, PyTorch, TensorFlow',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹8,00,000 - ₹25,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in AI, MS in Data Science, Ph.D. in Machine Learning',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Core CS & Math Education", "desc": "Complete a Bachelor's degree in Computer Science, Math, or Data Science."}, {"step": 2, "title": "Mathematical Foundations", "desc": "Master Linear Algebra, Probability, Statistics, and Calculus."}, {"step": 3, "title": "Core Machine Learning", "desc": "Learn regression, classification, clustering, and tree-based models using Scikit-Learn."}, {"step": 4, "title": "Deep Learning & Frameworks", "desc": "Master neural networks and deep learning models using PyTorch or TensorFlow."}, {"step": 5, "title": "Inference & Deployment", "desc": "Learn to build API endpoints and deploy models on cloud infrastructure like AWS or Azure."}])
        },
        {
            'title': 'Investment Banker',
            'stream': 'Commerce/Management',
            'description': 'Advise corporations and governments on financial strategies, execute mergers and acquisitions, and raise capital through debt and equity.',
            'required_skills': 'Financial Modeling, Investment Valuation, Excel, Analytical Thinking, Corporate Finance',
            'min_education': 'Undergraduate + MBA (Finance) / CFA',
            'salary_range': '₹10,00,000 - ₹35,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'CFA Charter, Executive MBA, Ph.D. in Finance',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Financial Foundations", "desc": "Complete a Bachelor's degree in Commerce, Economics, or Business Administration."}, {"step": 2, "title": "Valuation & Modeling skills", "desc": "Master advanced Excel, financial modeling, and corporate valuation tools."}, {"step": 3, "title": "Finance Specialization", "desc": "Obtain an MBA in Finance from a top school or register and clear CFA levels."}, {"step": 4, "title": "Securing Internships", "desc": "Secure summer analyst internships at boutique or bulge-bracket investment banks."}, {"step": 5, "title": "Financial Analyst Placement", "desc": "Join an investment bank division as a full-time Analyst, preparing pitch books and executing deals."}])
        },
        {
            'title': 'Veterinarian',
            'stream': 'Medical/Pharmacy',
            'description': 'Diagnose, treat, and prevent illnesses and injuries in domestic animals, livestock, and wildlife. Perform veterinary surgeries.',
            'required_skills': 'Animal Care, Clinical Medicine, Veterinary Surgery, Pharmacology, Pathology',
            'min_education': 'Undergraduate (BVSc & AH)',
            'salary_range': '₹4,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'MVSc (Master of Veterinary Science), Ph.D. in Veterinary Medicine',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Primary Sciences", "desc": "Complete Higher Secondary (12th) with Physics, Chemistry, and Biology."}, {"step": 2, "title": "Veterinary Degree", "desc": "Pass the national veterinary entrance exam and earn a BVSc & AH degree."}, {"step": 3, "title": "Clinical Rotations", "desc": "Undergo mandatory clinical training and veterinary internship rotations."}, {"step": 4, "title": "Professional Licensing", "desc": "Register with the State Veterinary Council to obtain a license to practice."}, {"step": 5, "title": "Clinical Practice", "desc": "Begin practicing at an animal clinic, corporate veterinary chain, or public livestock department."}])
        },
        {
            'title': 'Architect',
            'stream': 'Design/Arts',
            'description': 'Plan, design, and supervise the construction of residential, commercial, and public buildings. Ensure aesthetic and structural feasibility.',
            'required_skills': 'AutoCAD, SketchUp, Revit, Architectural Design, Space Planning, Blueprint Reading',
            'min_education': 'Undergraduate (B.Arch)',
            'salary_range': '₹4,00,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Moderate',
            'higher_studies_options': 'M.Arch, Master of Urban Planning, Project Management certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Architecture Degree", "desc": "Complete a 5-year Bachelor of Architecture (B.Arch) degree from a recognized council school."}, {"step": 2, "title": "Design Software Mastery", "desc": "Learn CAD and 3D modeling packages including AutoCAD, Revit, and SketchUp."}, {"step": 3, "title": "Council Registration", "desc": "Register with the Council of Architecture (CoA) to obtain your license."}, {"step": 4, "title": "Internship & Site Work", "desc": "Work as a junior architect to gain site supervision, space planning, and client experience."}, {"step": 5, "title": "Senior Designer / Partner", "desc": "Advance to Senior Architect, lead design modules, or launch your private practice."}])
        },
        {
            'title': 'Human Rights Lawyer',
            'stream': 'Law',
            'description': 'Advocate for civil liberties, defend human rights cases in courts, consult NGOs, and draft legal policies to protect vulnerable groups.',
            'required_skills': 'Constitutional Law, Legal Advocacy, Public Speaking, Legal Writing, Research',
            'min_education': 'Undergraduate (LLB/BA-LLB)',
            'salary_range': '₹3,50,000 - ₹10,00,000',
            'type': 'NGO / Public Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'LLM in Human Rights Law, Ph.D. in Law',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Acquire Law Degree", "desc": "Complete a 5-year integrated BA-LLB or a 3-year LLB degree from a law school."}, {"step": 2, "title": "Bar Council License", "desc": "Pass the All India Bar Examination (AIBE) to get a practice license."}, {"step": 3, "title": "Legal Aid Internships", "desc": "Intern with human rights NGOs, civil rights lawyers, or legal aid clinics."}, {"step": 4, "title": "Constitutional Practice", "desc": "Work as a junior advocate under a senior litigating human rights and constitutional law."}, {"step": 5, "title": "Advocacy & Consulting", "desc": "Represent cases in courts, consult for non-profits, or draft policies for international human rights commissions."}])
        }
,
        {
            'title': 'Blockchain Developer',
            'stream': 'Engineering/Technology',
            'description': 'Develop and implement secure blockchain protocols, smart contracts, and decentralized applications (dApps).',
            'required_skills': 'Solidity, Cryptography, Go, Rust, Web3.js, Smart Contracts',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹6,0,000 - ₹22,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'MS in Cryptographic Engineering, Blockchain Security Certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "CS & Programming Fundamentals", "desc": "Learn data structures, algorithms, and programming languages like Go or Rust."}, {"step": 2, "title": "Understand Cryptography & Blockchain", "desc": "Study public-key cryptography, hash functions, and consensus mechanisms."}, {"step": 3, "title": "Learn Solidity & Smart Contracts", "desc": "Write, compile, and test Solidity smart contracts on the Ethereum Virtual Machine (EVM)."}, {"step": 4, "title": "DApp Frontend Integration", "desc": "Build user interfaces that interact with blockchain nodes using Web3.js or Ethers.js."}, {"step": 5, "title": "Security Audits & Mainnet Deployment", "desc": "Learn security practices, gas optimizations, and deploy smart contracts on public testnets/mainnets."}])
        },
        {
            'title': 'DevOps Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Bridge the gap between software development and IT operations by automating builds, deployments, and cloud infrastructure.',
            'required_skills': 'Linux, Docker, Kubernetes, CI/CD, AWS, Terraform, Ansible',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹5,00,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'MS in Cloud Computing, AWS/Azure Solutions Architect Certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Linux & Scripting Foundations", "desc": "Master Linux system administration and shell scripting (Bash, Python)."}, {"step": 2, "title": "Version Control & CI/CD", "desc": "Understand Git workflow and automate integration/deployment using Jenkins or GitHub Actions."}, {"step": 3, "title": "Containerization", "desc": "Learn to package applications into secure, lightweight containers using Docker."}, {"step": 4, "title": "Container Orchestration & Infrastructure", "desc": "Manage multi-container applications at scale using Kubernetes and write Infrastructure-as-Code (Terraform)."}, {"step": 5, "title": "Cloud Administration & Monitoring", "desc": "Deploy resources to AWS/Azure and monitor system health using Prometheus and Grafana."}])
        },
        {
            'title': 'Embedded Systems Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design, develop, and test firmware and software that runs on electronic microcontrollers and hardware modules.',
            'required_skills': 'Embedded C, C++, Microcontrollers, RTOS, Microelectronics, Firmware, Oscilloscopes',
            'min_education': 'Undergraduate (B.Tech ECE/EEE/CS)',
            'salary_range': '₹4,00,000 - ₹14,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Moderate',
            'higher_studies_options': 'M.Tech in Embedded Systems, MS in Electrical and Computer Engineering',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Acquire Electrical & CS Bases", "desc": "Earn a degree in Electronics & Communication, Electrical Engineering, or Computer Science."}, {"step": 2, "title": "Master Embedded C & C++", "desc": "Learn C programming with a focus on memory management, register manipulation, and bitwise operations."}, {"step": 3, "title": "Understand Microcontroller Architecture", "desc": "Work with 8-bit/32-bit controllers (Arduino, STM32, ARM) and peripheral interfaces (I2C, SPI, UART)."}, {"step": 4, "title": "Real-Time Operating Systems (RTOS)", "desc": "Learn scheduling, task synchronization, and semaphore usage in RTOS platforms like FreeRTOS."}, {"step": 5, "title": "Hardware Debugging & Testing", "desc": "Learn to read schematics, use digital multi-meters, logic analyzers, and debug hardware signals."}])
        },
        {
            'title': 'Game Developer',
            'stream': 'Engineering/Technology',
            'description': 'Code game logic, physics engines, and graphics rendering using specialized frameworks and engines like Unity or Unreal.',
            'required_skills': 'C#, C++, Unity, Unreal Engine, Mathematics, Physics, Game Loop',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹3,50,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'MS in Game Design & Development, Graphics Programming certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Programming & Math Core", "desc": "Learn object-oriented programming (C# or C++) and vector mathematics/physics."}, {"step": 2, "title": "Learn Unity or Unreal Engine", "desc": "Choose Unity (C#) or Unreal (C++/Blueprints) and build basic 2D games."}, {"step": 3, "title": "Implement Game Mechanics", "desc": "Learn user input, collision detection, game state management, and basic AI behavior."}, {"step": 4, "title": "Asset & UI Integration", "desc": "Import 3D models, textures, animations, and construct interactive HUDs and menus."}, {"step": 5, "title": "Optimization & Publishing", "desc": "Optimize draw calls, frame rates, and export projects to PC, Web, or Mobile platforms."}])
        },
        {
            'title': 'Data Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Build, optimize, and maintain data pipelines, ETL architectures, and data warehouses to store and process large volumes of data.',
            'required_skills': 'SQL, Python, Spark, Hadoop, ETL Pipelines, Data Warehousing, Airflow',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹5,50,000 - ₹20,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in Data Engineering, Big Data Specializations',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Data Foundations", "desc": "Master SQL, relational database management, and Python programming."}, {"step": 2, "title": "Data Warehousing & Modeling", "desc": "Understand data architecture, normalization, star/snowflake schemas, and tools like Snowflake or Redshift."}, {"step": 3, "title": "ETL & Batch Processing", "desc": "Learn Extract, Transform, Load (ETL) concepts and write PySpark or Hadoop jobs."}, {"step": 4, "title": "Pipeline Orchestration", "desc": "Automate and schedule workflows using Apache Airflow or Prefect."}, {"step": 5, "title": "Real-Time Streaming", "desc": "Learn to build streaming data pipelines using Apache Kafka or Spark Streaming."}])
        },
        {
            'title': 'Site Reliability Engineer (SRE)',
            'stream': 'Engineering/Technology',
            'description': 'Apply software engineering practices to infrastructure and operations problems to build highly scalable and ultra-reliable software systems.',
            'required_skills': 'Python, Go, Kubernetes, Cloud Administration, Monitoring, Incident Response, Automation',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹7,00,000 - ₹24,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'MS in Cloud Systems, DevOps/SRE certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Systems Architecture", "desc": "Learn operating system design, networking protocols (TCP/IP, HTTP), and cloud architecture."}, {"step": 2, "title": "Infrastructure Automation", "desc": "Master Infrastructure-as-Code (Terraform) and Configuration Management (Ansible)."}, {"step": 3, "title": "Site Monitoring & SLIs", "desc": "Define Service Level Indicators (SLIs) and Service Level Objectives (SLOs) using Prometheus."}, {"step": 4, "title": "Reliability Patterns", "desc": "Implement fault-tolerance mechanisms, rate limiters, load balancing, and failover automation."}, {"step": 5, "title": "Incident Post-mortems", "desc": "Develop on-call practices, troubleshoot production incidents, and write blameless post-mortems."}])
        },
        {
            'title': 'Robotics Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design, build, program, and maintain automated machines, industrial robots, and autonomous vehicle control systems.',
            'required_skills': 'ROS (Robot Operating System), Python, C++, Microcontrollers, Kinematics, Control Systems, CAD',
            'min_education': 'Undergraduate (B.Tech Robotics/Mechatronics/ECE/CS)',
            'salary_range': '₹4,50,000 - ₹16,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Tech in Robotics, MS in Autonomous Systems',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Mechatronics Foundations", "desc": "Complete coursework in robotics, electrical circuits, and mechanical kinematics."}, {"step": 2, "title": "Robotics Software (ROS)", "desc": "Learn to use the Robot Operating System (ROS) in Python and C++ environments."}, {"step": 3, "title": "Sensors & Perception", "desc": "Interface with sensors like LiDAR, cameras, IMUs, and program computer vision algorithms."}, {"step": 4, "title": "Control Theory", "desc": "Implement PID controllers, motion planners, and path-finding algorithms."}, {"step": 5, "title": "Hardware Integration", "desc": "Assemble actuators, motor drivers, chassis systems, and execute physical robot calibration."}])
        },
        {
            'title': 'Cloud Security Specialist',
            'stream': 'Engineering/Technology',
            'description': 'Secure enterprise cloud environments, implement access management controls, and protect cloud infrastructure from security breaches.',
            'required_skills': 'Cloud Security, IAM, AWS Security, Network Security, Compliance, Vulnerability Assessment',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹6,00,000 - ₹20,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'CCSP (Certified Cloud Security Professional), CISSP',
            'roadmap_steps': json.dumps([{"step": 1, "title": "IT Security Basics", "desc": "Learn cryptography, network protocols, firewalls, and host security."}, {"step": 2, "title": "Cloud Architecture Mastery", "desc": "Learn cloud administration across AWS, Azure, or Google Cloud Platform."}, {"step": 3, "title": "Identity & Access Management", "desc": "Configure granular user policies, role-based access control (RBAC), and Single Sign-On (SSO)."}, {"step": 4, "title": "Security Compliance & Audits", "desc": "Study standards like SOC 2, ISO 27001, and perform vulnerability scanning."}, {"step": 5, "title": "Incident Response & Remediation", "desc": "Develop monitoring alerts and automated scripts to shut down exposed cloud services."}])
        },
        {
            'title': 'IoT Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design and program connected physical devices, sensors, and communication gateways that transmit data over networks.',
            'required_skills': 'IoT Protocols (MQTT CoAP), Embedded Systems, Python, C++, Network Communication, Cloud Integration',
            'min_education': 'Undergraduate (B.Tech ECE/EEE/CS)',
            'salary_range': '₹4,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Tech in IoT, Specialized Embedded Systems Training',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Circuit Design & Hardware", "desc": "Learn breadboarding, soldering, and basic microcontroller wiring (ESP8266/ESP32)."}, {"step": 2, "title": "Sensor Integration", "desc": "Program sensors to read temperatures, proximity, and GPS coordinates."}, {"step": 3, "title": "IoT Networking Protocols", "desc": "Understand MQTT, HTTP, and CoAP communication protocols."}, {"step": 4, "title": "Cloud Platform Integration", "desc": "Send telemetry data to IoT cloud hubs like AWS IoT, ThingSpeak, or Azure IoT."}, {"step": 5, "title": "Security & Optimization", "desc": "Implement secure device registration, firmware updates, and low-power operations."}])
        },
        {
            'title': 'Full Stack Developer',
            'stream': 'Engineering/Technology',
            'description': 'Build both the user-facing frontend and the server-side backend logic of responsive modern web applications.',
            'required_skills': 'React, Node.js, Express, HTML, CSS, JavaScript, SQL, MongoDB, REST APIs',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹4,50,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Advanced Web Architecture, Software Design Patterns',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Frontend Basics", "desc": "Master HTML, CSS, vanilla JavaScript, and modern DOM manipulation."}, {"step": 2, "title": "Frontend Frameworks", "desc": "Learn single-page application concepts using React, Vue, or Angular."}, {"step": 3, "title": "Backend Development", "desc": "Learn server-side scripting with Node.js and frameworks like Express."}, {"step": 4, "title": "Database Integration", "desc": "Connect servers to relational databases (SQL) or document stores (MongoDB)."}, {"step": 5, "title": "API Design & Deployment", "desc": "Build RESTful API endpoints, handle user authentication, and deploy to platforms like Heroku/AWS."}])
        },
        {
            'title': 'Bioinformatics Specialist',
            'stream': 'Science/Computer Applications',
            'description': 'Analyze genomic data sets, biological structures, and sequencing records using computational and statistical models.',
            'required_skills': 'Python, R, Genomics, Bioinformatics Databases, Statistics, Sequence Alignment',
            'min_education': 'Undergraduate (B.Sc Bioinformatics/Biotech/CS)',
            'salary_range': '₹4,00,000 - ₹11,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Sc in Bioinformatics, Ph.D. in Computational Biology',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Biological Science Basics", "desc": "Understand cell biology, genetics, DNA structure, and molecular sequencing."}, {"step": 2, "title": "Coding & Scripting Core", "desc": "Learn Python and R programming languages for managing files and datasets."}, {"step": 3, "title": "Genomics Tools & Libraries", "desc": "Utilize tools like BLAST, Biopython, and access databases like NCBI and UniProt."}, {"step": 4, "title": "Data Alignment & Analytics", "desc": "Execute sequence alignments, gene expression analysis, and phylogenetic trees."}, {"step": 5, "title": "Research Projects", "desc": "Perform independent computational bio-research or structural drug design simulations."}])
        },
        {
            'title': 'Quantitative Analyst',
            'stream': 'Science/Computer Applications',
            'description': 'Design mathematical and statistical algorithms for stock pricing, portfolio allocation, and risk management in financial firms.',
            'required_skills': 'Quantitative Finance, Python, C++, Statistics, Stochastic Calculus, Excel, Financial Modeling',
            'min_education': 'Undergraduate (B.Sc Math/Stats/B.Tech/BCA)',
            'salary_range': '₹8,0,000 - ₹30,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Sc in Quantitative Finance, Financial Engineering, Ph.D.',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Advanced Mathematics", "desc": "Master Linear Algebra, Probability theory, Calculus, and Statistics."}, {"step": 2, "title": "Scientific Programming", "desc": "Develop algorithms in Python, C++, or Matlab."}, {"step": 3, "title": "Financial Asset Valuation", "desc": "Learn Black-Scholes pricing model, bonds, options, and derivative pricing theory."}, {"step": 4, "title": "Stochastic Modeling", "desc": "Simulate stock prices and estimate risks using Monte Carlo methods."}, {"step": 5, "title": "Trading Systems & Algorithms", "desc": "Backtest quantitative strategies on historical market tick data."}])
        },
        {
            'title': 'AI Research Scientist',
            'stream': 'Science/Computer Applications',
            'description': 'Conduct research on new neural network architectures, generative models, and advanced machine learning theories.',
            'required_skills': 'Machine Learning, Deep Learning, PyTorch, Mathematical Modeling, Research Writing, Algorithms',
            'min_education': 'Postgraduate (M.Sc/M.Tech/Ph.D.)',
            'salary_range': '₹10,0,000 - ₹35,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Ph.D. in Artificial Intelligence or Cognitive Science',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Mathematical Modeling Foundations", "desc": "Master calculus, optimization algorithms, and advanced probability distributions."}, {"step": 2, "title": "Deep Learning Frameworks", "desc": "Become highly proficient in PyTorch, TensorFlow, and custom layer implementation."}, {"step": 3, "title": "Literature Review & Paper Studies", "desc": "Read and reproduce state-of-the-art AI papers published at NeurIPS, ICML, or CVPR."}, {"step": 4, "title": "Novel Architecture Design", "desc": "Propose modifications to model architectures, attention mechanisms, or loss functions."}, {"step": 5, "title": "Academic Publication", "desc": "Write academic papers, open-source models on HuggingFace, and defend research methodologies."}])
        },
        {
            'title': 'Forensic Scientist',
            'stream': 'Science/Computer Applications',
            'description': 'Collect, examine, and analyze physical and digital evidence related to criminal investigations.',
            'required_skills': 'Analytical Chemistry, DNA Profiling, Toxicology, Microscopic Examination, Crime Scene Investigation',
            'min_education': 'Undergraduate (B.Sc Forensic Science/Chemistry/BCA)',
            'salary_range': '₹3,0,000 - ₹8,0,000',
            'type': 'Government Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc in Forensic Science, Digital Forensics certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Forensics Education", "desc": "Earn a Bachelor of Science in Forensic Science, Biology, or Chemistry."}, {"step": 2, "title": "Laboratory Instrumentation", "desc": "Learn chromatography, mass spectrometry, and compound analysis."}, {"step": 3, "title": "Evidence Preservation", "desc": "Study protocols for chain of custody, fingerprints extraction, and DNA sampling."}, {"step": 4, "title": "Digital Forensics Fundamentals", "desc": "Learn tools for recovering files and inspecting system registries (FTK, EnCase)."}, {"step": 5, "title": "Expert Witness Training", "desc": "Learn courtroom procedures and report preparation for judicial review."}])
        },
        {
            'title': 'GIS Specialist',
            'stream': 'Science/Computer Applications',
            'description': 'Build, analyze, and maintain geographical maps and datasets using Geographic Information Systems software.',
            'required_skills': 'QGIS, ArcGIS, Python, Spatial Data Analysis, Cartography, Database Management',
            'min_education': 'Undergraduate (B.Sc Geoinformatics/Geography/BCA/B.Sc CS)',
            'salary_range': '₹3,50,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Sc in Geoinformatics, GIS Professional (GISP) certification',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Geographical Core", "desc": "Understand coordinate reference systems, map projections, and cartography principles."}, {"step": 2, "title": "Master GIS Desktop Software", "desc": "Learn standard mapping suites like ArcGIS Pro and QGIS."}, {"step": 3, "title": "Spatial Database Management", "desc": "Learn to query geographic datasets using PostgreSQL with PostGIS extensions."}, {"step": 4, "title": "Spatial Analysis Programming", "desc": "Write Python scripts using GDAL, Shapely, and GeoPandas for spatial processes."}, {"step": 5, "title": "Web Map Deployment", "desc": "Build web maps using Leaflet or OpenLayers frontend web frameworks."}])
        },
        {
            'title': 'Microbiologist',
            'stream': 'Science/Computer Applications',
            'description': 'Study microscopic organisms, including bacteria, viruses, fungi, and protozoa, to understand their roles in disease and ecology.',
            'required_skills': 'Aseptic Techniques, Microbial Culturing, Microscopy, PCR, Biosafety Protocols',
            'min_education': 'Undergraduate (B.Sc Microbiology/Biotech)',
            'salary_range': '₹3,0,000 - ₹7,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc in Microbiology, Ph.D. in Microbial Genetics',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Biology Foundations", "desc": "Understand biological systems, organic chemistry, and microbiology protocols."}, {"step": 2, "title": "Microbial Culturing & Isolation", "desc": "Practice sterile inoculation techniques, agar plates preparation, and staining."}, {"step": 3, "title": "Microscope Operations", "desc": "Learn light, fluorescent, and electron microscopy visualization methods."}, {"step": 4, "title": "Molecular Biology Analysis", "desc": "Perform DNA extraction, PCR gene amplification, and gel electrophoresis."}, {"step": 5, "title": "Quality Assurance & Biosafety", "desc": "Learn cleanroom standards and execute pharmaceutical/food purity tests."}])
        },
        {
            'title': 'Astrophysicist',
            'stream': 'Science/Computer Applications',
            'description': 'Study the physical properties and dynamics of stars, galaxies, black holes, and the universe using telescopes and physics simulations.',
            'required_skills': 'Physics, Calculus, Python, Data Analytics, Astronomy, Mathematical Simulation',
            'min_education': 'Postgraduate / Ph.D. (Physics/Astronomy)',
            'salary_range': '₹5,0,000 - ₹18,00,000',
            'type': 'Government Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'Post-Doctoral Fellowships, Academic Tenure Tracks',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Higher Physics & Calculus", "desc": "Master classical mechanics, electromagnetism, quantum mechanics, and advanced calculus."}, {"step": 2, "title": "Scientific Data Analysis", "desc": "Learn Python packages like Astropy, NumPy, and pandas to analyze astronomical data."}, {"step": 3, "title": "Telescope Instrumentation & Optics", "desc": "Learn to capture and clean signal noise from radio, optical, or space telescopes."}, {"step": 4, "title": "Cosmological Simulations", "desc": "Write high-performance computer models to simulate orbit dynamics or star formations."}, {"step": 5, "title": "Research Publications", "desc": "Write scientific papers and submit proposals to international observatory committees."}])
        },
        {
            'title': 'Statistician',
            'stream': 'Science/Computer Applications',
            'description': 'Apply mathematical statistics to collect, analyze, and present quantitative data to solve real-world problems in business and research.',
            'required_skills': 'Probability, Statistical Modeling, R, SAS, Excel, Data Analysis, Hypotheses Testing',
            'min_education': 'Undergraduate (B.Sc Statistics/Mathematics)',
            'salary_range': '₹4,0,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Sc in Statistics, Master of Data Science, Actuarial Science exam registration',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Mathematical Statistics bases", "desc": "Master algebra, probability distributions, and mathematical calculus."}, {"step": 2, "title": "Hypothesis & Sample Design", "desc": "Study parametric/non-parametric tests, t-tests, ANOVA, and survey designs."}, {"step": 3, "title": "Statistical Programming tools", "desc": "Learn R, SAS, or Python statistical libraries (Statsmodels, SciPy)."}, {"step": 4, "title": "Regression & Modeling", "desc": "Build linear, logistic, and multivariate regression models to discover data trends."}, {"step": 5, "title": "Business Reporting", "desc": "Interpret statistical outcomes and generate executive summaries with visual charts."}])
        },
        {
            'title': 'Environmental Scientist',
            'stream': 'Science/Computer Applications',
            'description': 'Study environmental pollution, sample water/soil qualities, and construct reports to protect ecosystems and human health.',
            'required_skills': 'Soil Sampling, Chemistry, Impact Assessment, Sustainability, GIS, Lab Analysis',
            'min_education': 'Undergraduate (B.Sc Environmental Science/Chemistry/Biology)',
            'salary_range': '₹3,0,000 - ₹9,00,000',
            'type': 'NGO / Public Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Sc in Environmental Engineering, Ph.D. in Sustainability Science',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Earth Science Basics", "desc": "Study ecosystems, chemistry, meteorology, and geologic structures."}, {"step": 2, "title": "Field Sampling Methods", "desc": "Learn soil core extraction, water pollution testing, and flora inventory mapping."}, {"step": 3, "title": "Chemical Analysis Labwork", "desc": "Run quantitative assays to detect toxic concentrations or heavy metals."}, {"step": 4, "title": "EIA Regulations", "desc": "Study Environmental Impact Assessment (EIA) standards and regional laws."}, {"step": 5, "title": "Report Writing & Compliance", "desc": "Write ecological audit reports for government approvals or conservation groups."}])
        },
        {
            'title': 'Geologist',
            'stream': 'Science/Computer Applications',
            'description': 'Study the composition, structure, and physical history of the Earth to discover mineral resources, oil fields, and map seismic hazards.',
            'required_skills': 'Mineralogy, Structural Geology, Field Mapping, GIS, Sedimentology, Safety Standards',
            'min_education': 'Undergraduate (B.Sc Geology/Earth Sciences)',
            'salary_range': '₹4,0,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc in Applied Geology, M.Tech in Petroleum Geosciences',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Geology Fundamentals", "desc": "Learn rock classification, geological timelines, and basic chemistry."}, {"step": 2, "title": "Field Mapping & Tools", "desc": "Learn to use geological compasses, record strike/dip, and trace formations."}, {"step": 3, "title": "Mineral Identification", "desc": "Identify minerals and rock structures under petrographic microscopes."}, {"step": 4, "title": "Geophysical Exploration", "desc": "Analyze seismic readouts, core logs, and gravitational anomalies."}, {"step": 5, "title": "Geotechnical Site Testing", "desc": "Analyze soil stability, water tables, and mineral resources for mining/construction."}])
        },
        {
            'title': 'Risk Manager',
            'stream': 'Commerce/Management',
            'description': 'Identify, analyze, and manage potential financial, operational, and regulatory risks that could impact business entities.',
            'required_skills': 'Risk Assessment, Financial Analysis, Compliance, Excel, Market Risk, Analytical Thinking',
            'min_education': 'Undergraduate (B.Com/BBA/B.Sc Math)',
            'salary_range': '₹5,0,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'FRM (Financial Risk Manager) Certification, MBA Finance',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Corporate Finance Core", "desc": "Learn accounting basics, statistical modeling, and microeconomics."}, {"step": 2, "title": "Risk Frameworks", "desc": "Understand market risk, credit risk, operational risk, and liquidity structures."}, {"step": 3, "title": "Risk Quantifications", "desc": "Learn to calculate Value-at-Risk (VaR) and perform financial stress testing."}, {"step": 4, "title": "Compliance & Basel Accords", "desc": "Study banking regulatory guidelines and internal audit procedures."}, {"step": 5, "title": "Hedging Strategies", "desc": "Formulate asset diversification or derivative hedging plans to lower exposures."}])
        },
        {
            'title': 'Supply Chain Analyst',
            'stream': 'Commerce/Management',
            'description': 'Analyze logistics, inventory management, and vendor relationships to optimize company supply chain cost and efficiency.',
            'required_skills': 'Data Analysis, Excel, Logistics, Supply Chain Management, Inventory Control, SAP',
            'min_education': 'Undergraduate (B.Com/BBA/B.Tech)',
            'salary_range': '₹3,50,000 - ₹11,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'APICS CSCP Certification, MBA in Supply Chain & Logistics',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Logistics & Supply Basics", "desc": "Learn supply chains concepts, freight carriers, warehousing, and purchase systems."}, {"step": 2, "title": "Master ERP Systems", "desc": "Learn to run logistics tracking and materials management modules in SAP or Oracle."}, {"step": 3, "title": "Inventory Management Analytics", "desc": "Use advanced Excel and database queries to monitor inventory turnovers."}, {"step": 4, "title": "Demand Forecasting", "desc": "Apply moving averages and predictive models to forecast product demand cycles."}, {"step": 5, "title": "Vendor Auditing & Contracts", "desc": "Negotiate pricing structures, set SLAs, and audit supplier delivery performances."}])
        },
        {
            'title': 'Brand Manager',
            'stream': 'Commerce/Management',
            'description': 'Define corporate brand guidelines, lead product packaging design, and execute advertising campaigns to drive market shares.',
            'required_skills': 'Brand Strategy, Market Research, Advertising, Marketing, Analytics, Communication',
            'min_education': 'Undergraduate + MBA (Marketing)',
            'salary_range': '₹6,0,000 - ₹20,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Advanced Brand Management, Digital PR masterclasses',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Marketing Bases", "desc": "Study consumer psychology, marketing mixes, and target demographic segments."}, {"step": 2, "title": "Market Research Analysis", "desc": "Conduct surveys, run focus groups, and inspect competitor positioning strategies."}, {"step": 3, "title": "Brand Guideline Drafting", "desc": "Design brand books, colors, typography rules, and coordinate packaging edits."}, {"step": 4, "title": "Campaign Budgeting & Launch", "desc": "Plan marketing campaign spending and coordinate with ad agencies for rollout."}, {"step": 5, "title": "Brand Equity Tracking", "desc": "Monitor customer retention rates, net promoter scores, and overall market share growth."}])
        },
        {
            'title': 'Business Development Manager',
            'stream': 'Commerce/Management',
            'description': 'Identify business partnerships, pitch corporate products to prospects, and expand client relationships to grow company revenues.',
            'required_skills': 'B2B Sales, Lead Generation, Negotiation, CRM (Salesforce), Presentation, Interpersonal Skills',
            'min_education': 'Undergraduate (BBA/B.Com/B.A)',
            'salary_range': '₹4,0,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'MBA in Business Strategy, Strategic Sales Leadership programs',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Sales & Pitching Basics", "desc": "Understand sales pipelines, lead nurturing, and client discovery questions."}, {"step": 2, "title": "Prospecting & Outreach", "desc": "Generate qualified leads via cold calling, email newsletters, and LinkedIn campaigns."}, {"step": 3, "title": "Master CRM Databases", "desc": "Learn CRM tools like Salesforce or Hubspot to track client communications."}, {"step": 4, "title": "Contracts & Proposals", "desc": "Draft commercial proposals and define pricing tiers for corporate partners."}, {"step": 5, "title": "Key Account Negotiation", "desc": "Conduct pitch presentations, resolve objections, and close commercial contracts."}])
        },
        {
            'title': 'Management Consultant',
            'stream': 'Commerce/Management',
            'description': 'Advise organizational managers on cost reductions, business restructuring, and process efficiencies.',
            'required_skills': 'Case Analysis, Business Strategy, Problem Solving, Presentation, Excel, Slide Design',
            'min_education': 'Undergraduate + MBA (from premier institutes)',
            'salary_range': '₹8,0,000 - ₹26,0,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Executive Certifications, Ph.D. in Business Strategy',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Strategic Management Theory", "desc": "Study Porter's Five Forces, MECE structures, and corporate case study solving."}, {"step": 2, "title": "Data Synthesis & Slide Work", "desc": "Build complex Excel tables and compile executive PowerPoint presentations."}, {"step": 3, "title": "Client Discovery Interviews", "desc": "Conduct surveys and interview front-line employees to spot organizational bottlenecks."}, {"step": 4, "title": "Financial modeling & Costing", "desc": "Evaluate operating costs and build financial models for new revenue branches."}, {"step": 5, "title": "Strategic Implementation Plan", "desc": "Deliver the transformation roadmap and consult client execution teams."}])
        },
        {
            'title': 'E-commerce Manager',
            'stream': 'Commerce/Management',
            'description': 'Coordinate website retail inventories, manage product uploads, optimize checkout conversion rates, and run digital sales campaigns.',
            'required_skills': 'Shopify, Google Analytics, Digital Marketing, Inventory Management, Customer Acquisition, A/B Testing',
            'min_education': 'Undergraduate (B.Com/BBA/B.A)',
            'salary_range': '₹4,0,000 - ₹13,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Specialized courses in E-Commerce Law or Conversion Rate Optimization (CRO)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "E-commerce Platforms", "desc": "Learn shop setup, theme customization, and plugin management in Shopify or WooCommerce."}, {"step": 2, "title": "Product Listing Optimization", "desc": "Write keyword-optimized product details and manage image uploads."}, {"step": 3, "title": "Traffic Acquisition", "desc": "Coordinate Google Shopping ads, email retargeting, and social media promotions."}, {"step": 4, "title": "Web Traffic Analytics", "desc": "Monitor bounce rates, cart abandonments, and average order values in Google Analytics."}, {"step": 5, "title": "Logistics & Checkout Integration", "desc": "Set up payment processors, shipping API rates, and optimize returns policies."}])
        },
        {
            'title': 'Tax Advisor',
            'stream': 'Commerce/Management',
            'description': 'Consult corporate clients or private individuals on filing income tax returns, using legal deductions, and minimizing tax liabilities.',
            'required_skills': 'Tax Laws (GST/Direct Tax), Accounting, Financial Auditing, Excel, Legal Compliance',
            'min_education': 'Undergraduate (B.Com/BBA) / CA',
            'salary_range': '₹3,50,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'Post Graduate Diploma in Taxation Law, Chartered Accountancy (CA)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Tax Law Bases", "desc": "Understand direct and indirect tax codes, corporate tax rates, and filing systems."}, {"step": 2, "title": "Financial Audit & Accounts", "desc": "Learn auditing checks, tax deduction codes, and balance sheet mapping."}, {"step": 3, "title": "Tax Return Filing Platforms", "desc": "Learn to use e-filing systems for GST, corporate, and individual income taxes."}, {"step": 4, "title": "Corporate Tax Planning", "desc": "Help companies save taxes legally using depreciation, investment, and research deductions."}, {"step": 5, "title": "Tax Dispute Representation", "desc": "Prepare answers to official tax department queries and represent clients in appeals."}])
        },
        {
            'title': 'Public Relations Specialist',
            'stream': 'Commerce/Management',
            'description': 'Draft corporate press releases, coordinate media interviews, and manage company reputation during public relations crises.',
            'required_skills': 'Media Relations, Press Releases, Crisis Communication, Copywriting, Public Relations, Interpersonal Skills',
            'min_education': 'Undergraduate (B.A. Journalism/BBA/B.Com)',
            'salary_range': '₹3,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Stable',
            'higher_studies_options': 'Postgraduate in Public Relations & Corporate Communication',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Media Communication Basics", "desc": "Study news cycles, journalist beats, and editorial styles."}, {"step": 2, "title": "Press Release Writing", "desc": "Learn to write newsworthy, concise corporate announcements."}, {"step": 3, "title": "Build Media Contact List", "desc": "Develop professional relationships with editors, reporters, and media figures."}, {"step": 4, "title": "Coordinate Press Conferences", "desc": "Set up media invitations, prepare media kits, and guide spokesperson talking points."}, {"step": 5, "title": "Crisis Management Strategy", "desc": "Draft holding messages, monitor negative news, and formulate company reply statements."}])
        },
        {
            'title': 'Financial Planner',
            'stream': 'Commerce/Management',
            'description': 'Consult individual clients on retirement savings, life insurance purchases, tax planning, and mutual fund asset allocations.',
            'required_skills': 'Investment Advisory, Financial Planning, Wealth Management, Excel, Communication, Market Knowledge',
            'min_education': 'Undergraduate (B.Com/BBA) & CFP Certification',
            'salary_range': '₹3,50,000 - ₹11,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'CFP (Certified Financial Planner) License, MBA Finance',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Personal Finance Basics", "desc": "Learn compounding interest, asset classes, mutual funds, and insurance types."}, {"step": 2, "title": "Financial Goal Calculations", "desc": "Use calculators and spreadsheets to find required target retirement corpuses."}, {"step": 3, "title": "Obtain CFP Certification", "desc": "Register and pass the Certified Financial Planner (CFP) certification exams."}, {"step": 4, "title": "Client Risk Assessment", "desc": "Evaluate client risk tolerances and suggest appropriate debt/equity asset allocations."}, {"step": 5, "title": "Annual Portfolio Review", "desc": "Conduct portfolio reviews, recommend rebalancing, and track tax-saving opportunities."}])
        },
        {
            'title': '3D Animator',
            'stream': 'Design/Arts',
            'description': 'Create moving digital characters, physics simulations, and environments for cinematic video games and commercial animations.',
            'required_skills': 'Maya, Blender, 3D Modeling, Rigging, Physics, Visual Storytelling, Keyframing',
            'min_education': 'Undergraduate (B.Des/BFA/Diploma in Animation)',
            'salary_range': '₹3,0,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'Advanced Character Rigging, MFA in Computer Animation',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Drawing & Anatomy Basics", "desc": "Practice manual drawing, perspective sketching, and anatomical proportions."}, {"step": 2, "title": "Learn Blender or Maya", "desc": "Understand the 3D workspace, basic modeling, texturing, and lighting configurations."}, {"step": 3, "title": "Master Rigging", "desc": "Create digital bone joints and weight maps to prepare character meshes for movement."}, {"step": 4, "title": "12 Principles of Animation", "desc": "Apply principles like squash/stretch, timing, and arcs to keyframe cycles."}, {"step": 5, "title": "Compile Demo Reel", "desc": "Build a 1-minute video portfolio showcasing character walks and action sequences."}])
        },
        {
            'title': 'Art Director',
            'stream': 'Design/Arts',
            'description': 'Lead the visual style and themes of advertising campaigns, magazines, movie sets, or video game projects.',
            'required_skills': 'Visual Communication, Design Leadership, Creative Direction, Typography, Adobe Suite, Concept Art',
            'min_education': 'Undergraduate (B.Des/BFA/Fine Arts)',
            'salary_range': '₹6,0,000 - ₹22,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Des, Specialized courses in Creative Leadership',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Visual Design Bases", "desc": "Master graphic design principles, color theories, typography, and copywriting."}, {"step": 2, "title": "Design Execution Work", "desc": "Spend 3-5 years working as a graphic designer or digital illustrator."}, {"step": 3, "title": "Concept Development", "desc": "Learn to translate marketing briefs into visual concepts and design boards."}, {"step": 4, "title": "Creative Team Leadership", "desc": "Manage designers, photographers, and copywriters to execute project deliverables."}, {"step": 5, "title": "Campaign Approvals", "desc": "Present creative directions to corporate stakeholders and sign off on print/digital releases."}])
        },
        {
            'title': 'Interior Designer',
            'stream': 'Design/Arts',
            'description': 'Plan spatial layouts, pick custom furniture, colors, lighting fixtures, and materials for residential and commercial building interiors.',
            'required_skills': 'AutoCAD, SketchUp, Space Planning, Materials, Lighting, Color Theory, Blueprint Reading',
            'min_education': 'Undergraduate (B.Des Interior/Diploma in Interior Design)',
            'salary_range': '₹3,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Des in Space Design, Specialized Lighting Design Certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Interior Design core", "desc": "Learn space dimensions, ergonomic standards, and scale drawing."}, {"step": 2, "title": "CAD & 3D Software", "desc": "Master AutoCAD for floor planning and SketchUp/V-Ray for 3D renders."}, {"step": 3, "title": "Materials & Procurement", "desc": "Study fabric selections, wood categories, light fixtures, and construct cost sheets."}, {"step": 4, "title": "Site Supervision", "desc": "Work with carpentry, plumbing, and painting contractors to verify drawings on-site."}, {"step": 5, "title": "Interior Portfolio Pitch", "desc": "Take high-quality photos of finished rooms and build a client portfolio."}])
        },
        {
            'title': 'Game Designer',
            'stream': 'Design/Arts',
            'description': 'Draft game rule books, design levels, plan combat math systems, and map overall user progression journeys.',
            'required_skills': 'Level Design, Game Mechanics, Narrative Design, Prototyping, Scripting, Game Balancing',
            'min_education': 'Undergraduate (B.Des Game Design/BCA/B.A)',
            'salary_range': '₹4,0,000 - ₹14,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Des in Game Design, Specialized courses in Game Analytics',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Play & Analyze Systems", "desc": "Play multiple game genres and dissect level progression paths and mechanics."}, {"step": 2, "title": "Write GDDs (Game Design Docs)", "desc": "Learn to write clear specs explaining controls, game loops, and UI structures."}, {"step": 3, "title": "Greybox Level Design", "desc": "Build test layout maps using primitive 3D cubes to evaluate player movements."}, {"step": 4, "title": "Scripting Basics", "desc": "Learn visual scripting (blueprints) or basic C# to prototype game rules."}, {"step": 5, "title": "Playtesting & Balance Tuning", "desc": "Gather player feedback, adjust game difficulties, and balance mechanics."}])
        },
        {
            'title': 'Industrial Designer',
            'stream': 'Design/Arts',
            'description': 'Design physical mass-produced products like consumer appliances, toy concepts, medical equipment, and automotive hulls.',
            'required_skills': 'SolidWorks, Keyshot, Concept Sketching, Ergonomics, Manufacturing Materials, Prototyping',
            'min_education': 'Undergraduate (B.Des Product/Industrial Design)',
            'salary_range': '₹4,0,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Des in Product Design, CAD/CAM advanced courses',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Design Sketching", "desc": "Learn rapid perspective sketching and product rendering with markers."}, {"step": 2, "title": "Product Ergonomics", "desc": "Study human dimensions and how individuals interact with physical shapes."}, {"step": 3, "title": "3D CAD Modeling", "desc": "Learn to build precise parametric surface models in SolidWorks or Rhino 3D."}, {"step": 4, "title": "Rapid Prototyping", "desc": "Create physical models using foam carving, laser cutting, or 3D printing."}, {"step": 5, "title": "Manufacturing DFM checks", "desc": "Study injection molding processes and review drafts for factory fabrication."}])
        },
        {
            'title': 'Motion Graphics Designer',
            'stream': 'Design/Arts',
            'description': 'Animate graphic shapes, kinetic typography, and logo designs for advertisements, film intros, and web apps.',
            'required_skills': 'After Effects, Illustrator, Photoshop, Motion Principles, Video Editing, Sound Design',
            'min_education': 'Undergraduate (B.Des/BFA/Diploma in Graphic Design)',
            'salary_range': '₹3,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Advanced 3D Motion Graphic workflows, Cinema 4D training',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Graphic Design Bases", "desc": "Master page layouts, color selection, vector curves, and typography."}, {"step": 2, "title": "Master After Effects", "desc": "Learn keyframing, parenting layers, expressions, and using vector shape tools."}, {"step": 3, "title": "Timing & Easing", "desc": "Understand the graph editor to smooth speed ramps and bounce trajectories."}, {"step": 4, "title": "Sound & Music Editing", "desc": "Add SFX, choose background music, and align animations to audio beats."}, {"step": 5, "title": "Video Demo Reel", "desc": "Combine 4-5 motion graphic clips into a video showcase page."}])
        },
        {
            'title': 'Textile Designer',
            'stream': 'Design/Arts',
            'description': 'Create design patterns, print layouts, and weave structures for apparel fabrics, carpets, and interior linens.',
            'required_skills': 'Pattern Design, Textile Weaving, Photoshop, Illustrator, Dyeing Processes, Material Sciences',
            'min_education': 'Undergraduate (B.Des Textile Design/Diploma in Fashion Tech)',
            'salary_range': '₹2,50,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Des in Textile Design, Specialized eco-friendly fabric courses',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Fiber & Yarn Science", "desc": "Study cotton, wool, silk, and synthetic fibers, and how they are woven."}, {"step": 2, "title": "Repeat Pattern Drawing", "desc": "Design repeating print patterns and color separations in Photoshop/Illustrator."}, {"step": 3, "title": "Weave Structure CAD", "desc": "Learn to design woven structural drafts using loom software."}, {"step": 4, "title": "Fabric Dyeing & Printing", "desc": "Practice screen printing, block printing, and chemical dyeing."}, {"step": 5, "title": "Apparel & Furnishing Fit", "desc": "Design and apply custom prints onto apparel prototypes or room mockups."}])
        },
        {
            'title': 'Exhibition Designer',
            'stream': 'Design/Arts',
            'description': 'Design public exhibition stalls, museum galleries, trade show booths, and retail merchandise displays.',
            'required_skills': 'AutoCAD, 3D Rendering, Spatial Layout, Lighting, Material Specs, Brand Integration',
            'min_education': 'Undergraduate (B.Des/B.Arch/Fine Arts)',
            'salary_range': '₹3,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Des, Specialized courses in Event Architecture',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Architectural Space Basics", "desc": "Understand human traffic paths, structural safety, and elevation scales."}, {"step": 2, "title": "CAD & 3D Drafting", "desc": "Learn to draft booth plans and output 3D views in AutoCAD and 3ds Max."}, {"step": 3, "title": "Exhibition Lighting & Signage", "desc": "Design brand signs, spot lighting arrays, and print graphics."}, {"step": 4, "title": "Material Specifications", "desc": "Select lightweight panels, acrylic frames, and trace structural blueprints."}, {"step": 5, "title": "On-Site Installation", "desc": "Coordinate construction vendors on the exhibition hall floor to set up display stalls."}])
        },
        {
            'title': 'Intellectual Property (IP) Lawyer',
            'stream': 'Law',
            'description': 'Advise clients on patent registrations, register corporate trademarks, defend copyrights, and litigate IP infringement disputes.',
            'required_skills': 'Patent Law, Trademark Filing, Copyright Act, Legal Writing, Litigation, Negotiation',
            'min_education': 'Undergraduate (LLB/BA-LLB)',
            'salary_range': '₹5,0,000 - ₹22,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'LLM in Intellectual Property Law, Patent Agent Registration Exam',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Earn Law Degree", "desc": "Graduate with an LLB or integrated BA-LLB, preferably with courses in science/tech."}, {"step": 2, "title": "Patent & Trademark Code", "desc": "Study Patents Act, Trademarks Act, and international IP treaty frameworks."}, {"step": 3, "title": "IP Filing Clerkships", "desc": "Intern at specialized IP law firms, drafting patent claims and trademark objections."}, {"step": 4, "title": "Bar Council License", "desc": "Pass the Bar exam to practice in courts."}, {"step": 5, "title": "IP Litigations & Portfolio Management", "desc": "Represent infringement cases in High Courts and handle global trademark renewals."}])
        },
        {
            'title': 'Environmental Lawyer',
            'stream': 'Law',
            'description': 'Represent environmental groups, advice corporate clients on carbon/waste regulations, and litigate climate conservation filings in tribunals.',
            'required_skills': 'Environmental Laws, NGT Rules, Public Interest Litigation (PIL), Research, Legal Advocacy',
            'min_education': 'Undergraduate (LLB/BA-LLB)',
            'salary_range': '₹4,0,000 - ₹12,00,000',
            'type': 'NGO / Public Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'LLM in Environmental Law, Ph.D. in Resource Jurisprudence',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Environmental Statutes", "desc": "Study Air/Water pollution acts, Forest Conservation rules, and the NGT Act."}, {"step": 2, "title": "Internships with Green NGOs", "desc": "Intern with public interest litigation lawyers at National Green Tribunals."}, {"step": 3, "title": "Legal Compliance Audits", "desc": "Learn to inspect corporate environmental audits and emissions clearances."}, {"step": 4, "title": "Drafting PIL Petitions", "desc": "Draft public interest litigations challenging illegal mining or river dumping."}, {"step": 5, "title": "Tribunal Practice", "desc": "Secure practice rights and represent ecological conservation disputes in courts."}])
        },
        {
            'title': 'Criminal Lawyer',
            'stream': 'Law',
            'description': 'Defend or prosecute individuals accused of criminal violations, conduct cross-examinations, and manage bail trials.',
            'required_skills': 'Criminal Procedure (CrPC), IPC, Cross-Examination, Criminal Defense, Oral Advocacy, Investigation',
            'min_education': 'Undergraduate (LLB/BA-LLB)',
            'salary_range': '₹3,0,000 - ₹18,00,000',
            'type': 'NGO / Public Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'LLM in Criminal Law, Specialized forensic training courses',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Criminal Jurisprudence", "desc": "Study Penal Codes, Criminal Procedure, and Evidence Acts."}, {"step": 2, "title": "Trial Court Clerkships", "desc": "Intern under active trial court lawyers, attending daily bail and evidence hearings."}, {"step": 3, "title": "Drafting Court Pleadings", "desc": "Draft bail applications, criminal appeals, and witness cross-examination files."}, {"step": 4, "title": "Bar License Registration", "desc": "Clear state bar exam to secure legal practice rights."}, {"step": 5, "title": "Independent Practice", "desc": "Represent client defenses in court trials and perform cross-examinations."}])
        },
        {
            'title': 'Cyber Lawyer',
            'stream': 'Law',
            'description': 'Advise clients on data privacy compliance, prosecute online financial fraud cases, and represent data leak disputes.',
            'required_skills': 'Information Technology Act, Data Privacy Laws, Digital Evidence, Cybersecurity, Legal Drafting',
            'min_education': 'Undergraduate (LLB/BA-LLB) / Diploma in Cyber Law',
            'salary_range': '₹4,0,000 - ₹16,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'LLM in Technology Law, Certifications in GDPR/ISO 27001',
            'roadmap_steps': json.dumps([{"step": 1, "title": "IT & Data Statutes", "desc": "Master IT Acts, digital signature guidelines, and data protection rules."}, {"step": 2, "title": "Digital Forensics basics", "desc": "Learn how digital evidence is retrieved, preserved, and presented in court."}, {"step": 3, "title": "Cyber Cell Internships", "desc": "Intern with police cyber cells or tech law firms advising on data policies."}, {"step": 4, "title": "Compliance Program Audits", "desc": "Draft privacy policies, terms of service, and audit compliance for SaaS brands."}, {"step": 5, "title": "Court Trial Litigations", "desc": "Represent client cyber fraud defenses or data breach actions in courts."}])
        },
        {
            'title': 'Dentist',
            'stream': 'Medical/Pharmacy',
            'description': 'Diagnose and treat dental diseases, perform teeth restorations, oral surgeries, and fit cosmetic prosthetics.',
            'required_skills': 'Oral Diagnosis, Dental Surgery, Orthodontics, Patient Care, Medical Hygiene, Clinical Diagnosis',
            'min_education': 'Undergraduate (BDS)',
            'salary_range': '₹3,0,000 - ₹12,0,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'MDS (Master of Dental Surgery), Specialized Cosmetic Dentistry fellowships',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Dental Degree", "desc": "Earn a Bachelor of Dental Surgery (BDS) from a recognized dental college."}, {"step": 2, "title": "Clinical Rotations", "desc": "Complete mandatory 1-year rotational clinical internship at hospital wards."}, {"step": 3, "title": "Dental Council Licensing", "desc": "Register with the State Dental Council to secure a dental practice license."}, {"step": 4, "title": "Join Dental Clinic", "desc": "Work as an associate dentist to master extraction and root canal treatments."}, {"step": 5, "title": "Open Private Clinic", "desc": "Set up a private dental practice with diagnostic chair and imaging equipment."}])
        },
        {
            'title': 'Physiotherapist',
            'stream': 'Medical/Pharmacy',
            'description': 'Rehabilitate patients recovering from physical injuries, surgeries, or chronic movement disorders using physical exercises.',
            'required_skills': 'Physiotherapy, Anatomy, Kinesiology, Injury Rehabilitation, Patient Care, Exercise Therapy',
            'min_education': 'Undergraduate (BPT)',
            'salary_range': '₹2,50,000 - ₹8,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'MPT (Master of Physiotherapy), Sports Physiotherapy specializations',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Physiotherapy Degree", "desc": "Complete a 4.5-year Bachelor of Physiotherapy (BPT) program."}, {"step": 2, "title": "Anatomy & Physiology Core", "desc": "Study muscle kinematics, neural paths, and orthopedic diagnoses."}, {"step": 3, "title": "Supervised Internships", "desc": "Intern at hospital physical therapy divisions, handling traction and mobilization."}, {"step": 4, "title": "Council Registration", "desc": "Register with the regional association to secure a physiotherapy practice license."}, {"step": 5, "title": "Clinical Practice", "desc": "Join sports rehabilitation centers or start a home-visit physical therapy service."}])
        },
        {
            'title': 'Clinical Research Associate',
            'stream': 'Medical/Pharmacy',
            'description': 'Supervise clinical drug trials, verify hospital protocol compliance, and monitor patient safety logs for pharmaceutical developers.',
            'required_skills': 'Clinical Trials, GCP Guidelines, Clinical Data Management, Pharmacology, Auditing',
            'min_education': 'Undergraduate (B.Pharm/B.Sc Biotech/MBBS)',
            'salary_range': '₹3,50,000 - ₹9,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'Postgraduate Diploma in Clinical Research, M.Pharm',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Pharmacy/Life Sciences Degree", "desc": "Graduate with a B.Pharm, B.Sc Biotech, or BDS/MBBS degree."}, {"step": 2, "title": "Learn GCP Guidelines", "desc": "Master Good Clinical Practice (GCP) codes and trial methodologies."}, {"step": 3, "title": "Clinical Site Monitoring", "desc": "Intern at clinical research sites, verifying patient informed consent forms."}, {"step": 4, "title": "Case Report Audit", "desc": "Audit patient source documents against clinical databases for consistency."}, {"step": 5, "title": "Lead Clinical Trials", "desc": "Join a CRO (Contract Research Org) to manage multi-center drug studies."}])
        },
        {
            'title': 'Epidemiologist',
            'stream': 'Medical/Pharmacy',
            'description': 'Investigate patterns, causes, and transmission routes of infectious diseases in populations to define healthcare policies.',
            'required_skills': 'Epidemiology, Biostatistics, Public Health, Data Analysis, Disease Control, Research Methods',
            'min_education': 'Postgraduate (MPH / M.Sc Epidemiology)',
            'salary_range': '₹4,50,000 - ₹14,00,000',
            'type': 'Government Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'Ph.D. in Public Health or Epidemiology',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Public Health Foundations", "desc": "Complete a medical degree (MBBS/BDS) or B.Sc in Biological Sciences."}, {"step": 2, "title": "Master of Public Health", "desc": "Earn an MPH or M.Sc in Epidemiology from a recognized institute."}, {"step": 3, "title": "Statistical Software (SAS/R)", "desc": "Learn stats computing to analyze disease registry data."}, {"step": 4, "title": "Outbreak Field Investigations", "desc": "Participate in field surveys to trace contagion paths and source variables."}, {"step": 5, "title": "Public Health Policy Drafts", "desc": "Formulate disease prevention policies for government health departments or WHO."}])
        },
        {
            'title': 'Pharmacovigilance Specialist',
            'stream': 'Medical/Pharmacy',
            'description': 'Monitor post-market pharmaceutical products, log drug side-effects, and file adverse event reports to safety commissions.',
            'required_skills': 'Drug Safety, Adverse Event Reporting, Medical Coding (MedDRA), Pharmacology, Database Management',
            'min_education': 'Undergraduate (B.Pharm/M.Pharm/Pharm.D)',
            'salary_range': '₹3,0,000 - ₹8,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'Advanced Pharmacovigilance, Regulatory Affairs certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Pharmacy/Medical Education", "desc": "Graduate with a B.Pharm, M.Pharm, BDS, or Pharm.D degree."}, {"step": 2, "title": "Pharmacovigilance Codes", "desc": "Understand ICH guidelines and global regulatory safety rules."}, {"step": 3, "title": "Adverse Event Processing", "desc": "Learn to log patient safety complaints in databases like Argus or ArisG."}, {"step": 4, "title": "Medical Coding (MedDRA)", "desc": "Learn to code clinical side-effects using standard MedDRA dictionaries."}, {"step": 5, "title": "Signal Detection & Reporting", "desc": "Evaluate adverse event trends and construct official safety files."}])
        },
        {
            'title': 'Curriculum Designer',
            'stream': 'Education/Humanities',
            'description': 'Design school course syllabi, select textbooks, and construct digital learning modules for academic schools.',
            'required_skills': 'Curriculum Design, Instructional Design, Lesson Planning, Educational Psychology, Content Development',
            'min_education': 'Undergraduate + B.Ed / M.Ed',
            'salary_range': '₹3,50,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'Ph.D. in Education or Curriculum Studies',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Teaching Foundations", "desc": "Earn a Bachelor's degree followed by a B.Ed or M.Ed in education."}, {"step": 2, "title": "Classroom Instruction Work", "desc": "Spend 2-4 years teaching in secondary or higher secondary classrooms."}, {"step": 3, "title": "Instructional Design Theories", "desc": "Study learning taxonomies (Bloom's Taxonomy) and course structure rules."}, {"step": 4, "title": "E-Learning Authoring Tools", "desc": "Learn course publishing programs like Articulate Storyline or Adobe Captivate."}, {"step": 5, "title": "Curriculum Assessment", "desc": "Formulate student test rubrics and run educational impact audits."}])
        },
        {
            'title': 'Event Planner',
            'stream': 'Hotel Management/Vocational',
            'description': 'Coordinate venue bookings, manage catering menus, arrange decorators, and supervise timelines for weddings and corporate conferences.',
            'required_skills': 'Event Management, Budgeting, Vendor Management, Customer Relations, Operations',
            'min_education': 'Undergraduate (BHM/BBA/Diploma in Event Management)',
            'salary_range': '₹3,0,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Growing',
            'higher_studies_options': 'Advanced Corporate Event Management, Venue Marketing programs',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Hospitality Core", "desc": "Learn hospitality basics, catering logistics, and floor planning."}, {"step": 2, "title": "Supplier Relations", "desc": "Build a contact list of caterers, decorators, light technicians, and sound bands."}, {"step": 3, "title": "Budget Spreadsheet Mastery", "desc": "Learn to design detailed client event cost models and profit charts."}, {"step": 4, "title": "On-Site Coordination", "desc": "Manage live wedding timelines, guest reception tables, and vendor deliveries."}, {"step": 5, "title": "Event Agency Lead", "desc": "Market planning packages to clients or run an independent event company."}])
        },
        {
            'title': 'Fitness Trainer',
            'stream': 'Hotel Management/Vocational',
            'description': 'Design personalized strength routines, consult client nutrition choices, and lead group fitness classes in gyms.',
            'required_skills': 'Exercise Physiology, Strength Training, Nutrition, Client Coaching, First Aid/CPR',
            'min_education': 'Higher Secondary + Certified Fitness Trainer certification',
            'salary_range': '₹2,0,000 - ₹7,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Growing',
            'higher_studies_options': 'CSCS (Certified Strength and Conditioning Specialist), Sports Nutrition certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Anatomy & Fitness Basics", "desc": "Study basic muscle systems, compound lifting movements, and cardio targets."}, {"step": 2, "title": "Trainer Certification", "desc": "Pass a recognized personal trainer certification exam (ACE, ACSM, or Gold's Gym)."}, {"step": 3, "title": "Nutrition Coaching", "desc": "Learn macronutrient distributions, calorie calculation, and hydration rules."}, {"step": 4, "title": "Client Assessment", "desc": "Conduct body fat scans, evaluate posture limits, and create custom routines."}, {"step": 5, "title": "Freelance Personal Training", "desc": "Deliver personal coaching services, build client success histories, or manage a gym floor."}])
        }
,
        {
            'title': 'Investment Analyst',
            'stream': 'Commerce/Management',
            'description': 'Evaluate financial statements, stock market indicators, and macroeconomic charts to recommend buy/sell assets for funds.',
            'required_skills': 'Financial Analysis, Equity Research, Financial Modeling, Valuations, Excel, SEC Filings',
            'min_education': 'Undergraduate (B.Com/BBA/B.Sc Finance)',
            'salary_range': '₹5,0,000 - ₹16,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'CFA (Chartered Financial Analyst), MBA Finance',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Accounting Foundations", "desc": "Master balance sheets, income statements, and cash flow statement reconciliations."}, {"step": 2, "title": "Market Data Databases", "desc": "Learn terminal applications like Bloomberg or Capital IQ to extract financial datasets."}, {"step": 3, "title": "Discounted Cash Flow Model", "desc": "Build comprehensive DCF and comparable company valuation models in Excel."}, {"step": 4, "title": "Write Equity Research Report", "desc": "Draft buy/sell stock thesis, highlighting product line expansions and macro risks."}, {"step": 5, "title": "Portfolio Advisory Pitch", "desc": "Present stock research summaries to investment committee leads."}])
        }
,
        {
            'title': 'Aerospace Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Design, construct, and test aircraft, missiles, satellites, and spacecraft systems.',
            'required_skills': 'Aerodynamics, CAD, Propulsion, Matlab, Systems Engineering, Fluid Dynamics',
            'min_education': 'Undergraduate (B.Tech Aerospace/Mechanical)',
            'salary_range': '₹5,00,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'M.Tech in Aerospace Dynamics, MS in Space Systems',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Aerospace Core", "desc": "Complete coursework in thermodynamics, propulsion, and structural analysis."}, {"step": 2, "title": "Simulations Software", "desc": "Learn CAD modeling and aerodynamic simulation tools like ANSYS Fluent."}, {"step": 3, "title": "Aerospace Internships", "desc": "Intern with aviation groups, space research bodies, or commercial airlines."}, {"step": 4, "title": "Avionics Integration", "desc": "Study control systems, navigation dynamics, and sensor calibrations."}, {"step": 5, "title": "Systems Engineer Placement", "desc": "Join aerospace design teams for manufacturing design reviews."}])
        },
        {
            'title': 'QA Automation Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Write automated test scripts to validate software quality, performance, and API responses.',
            'required_skills': 'Selenium, Java, Python, Cypress, API Testing, Git, Test Automation',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹4,00,000 - ₹14,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Advanced Software Architecture, Cloud QA Certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Programming Basics", "desc": "Learn Java, Python, or JavaScript coding fundamentals."}, {"step": 2, "title": "Software Testing Basics", "desc": "Understand bug reporting, test cases, regressions, and manual test strategies."}, {"step": 3, "title": "Automation Frameworks", "desc": "Master Selenium Webdriver, Cypress, or Playwright to automate browser workflows."}, {"step": 4, "title": "API & CI/CD pipeline tests", "desc": "Learn API testing (Postman) and integrate test suites into Jenkins/GitHub Actions."}, {"step": 5, "title": "Lead QA role", "desc": "Establish QA metrics, cross-browser dashboards, and coordinate release approvals."}])
        },
        {
            'title': 'Database Architect',
            'stream': 'Engineering/Technology',
            'description': 'Design, construct, and optimize enterprise-scale relational and non-relational database schemas.',
            'required_skills': 'SQL, Database Design, NoSQL, Oracle, PostgreSQL, Performance Tuning, Sharding',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹6,50,000 - ₹24,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Database Administrator Certifications, MS in Data Systems',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Database Normalization", "desc": "Master entity schemas, relationship models, and keys."}, {"step": 2, "title": "Advanced SQL Queries", "desc": "Write complex joins, nested subqueries, and database procedures."}, {"step": 3, "title": "NoSQL & Scalability", "desc": "Learn document stores (MongoDB) and key-value caches (Redis)."}, {"step": 4, "title": "Performance Optimization", "desc": "Learn query indexing, execution plans, and data sharding methods."}, {"step": 5, "title": "Enterprise Architecture", "desc": "Design high-availability clusters and write recovery strategies."}])
        },
        {
            'title': 'Computer Vision Engineer',
            'stream': 'Engineering/Technology',
            'description': 'Develop image processing and deep learning models to enable computers to extract features from digital images or videos.',
            'required_skills': 'OpenCV, Python, PyTorch, Convolutional Neural Networks, Deep Learning, Image Processing',
            'min_education': 'Undergraduate (B.Tech/BCA/B.Sc CS)',
            'salary_range': '₹7,00,000 - ₹25,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'M.Tech in Artificial Intelligence, Ph.D. in Computer Vision',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Core Math & Python", "desc": "Master linear algebra, matrices, calculus, and Python."}, {"step": 2, "title": "Classical Image Processing", "desc": "Learn edge detection, filtering, and thresholding using OpenCV."}, {"step": 3, "title": "Deep Learning for Vision", "desc": "Study Convolutional Neural Networks (CNNs) and transfer learning."}, {"step": 4, "title": "Object Detection Frameworks", "desc": "Deploy object detectors like YOLO, SSD, or Mask R-CNN."}, {"step": 5, "title": "Edge Deployment", "desc": "Optimize models using ONNX or TensorRT for deployment on embedded devices."}])
        },
        {
            'title': 'Materials Scientist',
            'stream': 'Science/Computer Applications',
            'description': 'Study the molecular structures and properties of materials like metals, polymers, and ceramics to design new products.',
            'required_skills': 'Materials Characterization, Metallurgy, Polymer Chemistry, Nanotechnology, Spectroscopy',
            'min_education': 'Undergraduate (B.Sc Chemistry/Physics/Materials)',
            'salary_range': '₹3,50,000 - ₹11,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc/M.Tech in Materials Science, Ph.D.',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Physics & Chemistry bases", "desc": "Study crystalline structures, thermodynamic properties, and organic chemistry."}, {"step": 2, "title": "Material Characterization Labwork", "desc": "Practice SEM imaging, X-ray diffraction, and tensile testing."}, {"step": 3, "title": "Nanomaterials study", "desc": "Research properties of carbon nanotubes, graphene, and quantum dots."}, {"step": 4, "title": "Polymer Synthesis", "desc": "Learn polymerization mechanics and properties of plastics."}, {"step": 5, "title": "Industrial R&D", "desc": "Join product development labs to formulate stronger, lighter composite alloys."}])
        },
        {
            'title': 'Actuarial Analyst',
            'stream': 'Science/Computer Applications',
            'description': 'Evaluate financial risks using mathematical probability, statistics, and financial modeling for insurance providers.',
            'required_skills': 'Probability, Statistical Modeling, Financial Math, Excel, Actuarial Exams, Risk Analysis',
            'min_education': 'Undergraduate (B.Sc Math/Stats/B.Com)',
            'salary_range': '₹5,00,000 - ₹20,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'High',
            'higher_studies_options': 'Institute of Actuaries Exams (Fellowship level)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Advanced Mathematics", "desc": "Master probability theory, financial calculus, and mathematical statistics."}, {"step": 2, "title": "Pass Initial Actuarial Exams", "desc": "Register with the Actuarial Institute and pass Core Mathematics/Statistics papers."}, {"step": 3, "title": "Excel & Risk Modeling", "desc": "Learn database queries, complex macro scripting, and cohort mortality calculations."}, {"step": 4, "title": "Insurance Product Pricing", "desc": "Calculate policy premiums and safety reserve levels for health/life portfolios."}, {"step": 5, "title": "Actuary Charter", "desc": "Complete all remaining paper sets to secure Fellow status."}])
        },
        {
            'title': 'Clinical Data Manager',
            'stream': 'Science/Computer Applications',
            'description': 'Ensure clinical trial databases are constructed securely, collect clinical profiles, and audit data entries for GCP compliance.',
            'required_skills': 'Clinical Data Management, CDISC Standards, SQL, GCP, SAS, Database Auditing',
            'min_education': 'Undergraduate (B.Sc CS/Bio/B.Pharm/BCA)',
            'salary_range': '₹3,50,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'Postgraduate in Clinical Data Management',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Sciences Core", "desc": "Graduate with a degree in science, computer applications, or pharmacy."}, {"step": 2, "title": "CDM Systems", "desc": "Learn Electronic Data Capture (EDC) systems used in clinical settings."}, {"step": 3, "title": "Database Design & Validation", "desc": "Design Case Report Forms (CRFs) and set up logical validation checks."}, {"step": 4, "title": "Data Cleansing & CDISC", "desc": "Query discrepant entries, compile audit trails, and format data for CDISC submission."}, {"step": 5, "title": "Study Database Lock", "desc": "Execute database lock controls and compile data reports for reviewers."}])
        },
        {
            'title': 'Research Analyst',
            'stream': 'Science/Computer Applications',
            'description': 'Gather, format, and evaluate quantitative data for research institutions, think-tanks, or equity companies.',
            'required_skills': 'Data Gathering, Quantitative Research, Excel, Statistics, Report Writing, Presentation',
            'min_education': 'Undergraduate (B.Sc/BCA/B.A Economics)',
            'salary_range': '₹3,00,000 - ₹9,50,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Sc in Applied Economics, MBA, CFA',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Research Methodology", "desc": "Study sampling designs, survey methods, and qualitative/quantitative theory."}, {"step": 2, "title": "Spreadsheet Analytics", "desc": "Master Excel lookups, pivot tables, and statistical formulas."}, {"step": 3, "title": "Market & Trend Analysis", "desc": "Gather data from reports, inspect macro factors, and monitor competitor lines."}, {"step": 4, "title": "Report Writing", "desc": "Draft objective research briefs explaining findings with charts and tables."}, {"step": 5, "title": "Strategy Consulting", "desc": "Deliver insights to corporate panels to guide organizational direction."}])
        },
        {
            'title': 'Internal Auditor',
            'stream': 'Commerce/Management',
            'description': 'Examine company operating records, ledger accounts, and internal controls to verify policy compliance and prevent fraud.',
            'required_skills': 'Internal Auditing, Accounting Standards, Risk Assessment, Compliance, Excel, Report Writing',
            'min_education': 'Undergraduate (B.Com/BBA)',
            'salary_range': '₹3,50,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'CIA (Certified Internal Auditor) License, CA',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Accounting bases", "desc": "Study corporate bookkeeping, balance sheet matching, and costing methods."}, {"step": 2, "title": "Audit Frameworks", "desc": "Learn risk-based auditing methodologies and corporate compliance codes."}, {"step": 3, "title": "Process Walkthroughs", "desc": "Interview team leads to trace transaction processes and locate loopholes."}, {"step": 4, "title": "Substantive Testing", "desc": "Collect sample vouchers, verify receipts, and perform financial checks."}, {"step": 5, "title": "Auditing Reports", "desc": "Draft audit summaries, present internal weaknesses to directors, and track corrections."}])
        },
        {
            'title': 'Operations Manager',
            'stream': 'Commerce/Management',
            'description': 'Supervise daily activities, optimize business processes, and manage operating budgets in corporate environments.',
            'required_skills': 'Operations Management, Process Optimization, Budgeting, Leadership, Project Management',
            'min_education': 'Undergraduate + MBA (Operations)',
            'salary_range': '₹5,00,000 - ₹18,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Six Sigma Black Belt Certification, PMP',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Business Management core", "desc": "Study microeconomics, human resources, and business finance basics."}, {"step": 2, "title": "Project Management tools", "desc": "Learn tracking frameworks (Gantt charts, Agile sprint setups) and tools like Jira."}, {"step": 3, "title": "Process Optimization (Lean)", "desc": "Study Lean principles, mapping workflows, and cost reduction strategies."}, {"step": 4, "title": "Department Budgeting", "desc": "Manage quarterly operational budgets and coordinate supply/staff procurement."}, {"step": 5, "title": "Operations Lead", "desc": "Optimize overall organizational workflows and present progress charts to executives."}])
        },
        {
            'title': 'Media Planner',
            'stream': 'Commerce/Management',
            'description': 'Plan corporate advertising spots across television, social media, radio, and magazines to optimize reach for campaigns.',
            'required_skills': 'Media Strategy, Budget Allocation, Market Research, Negotiation, Analytics, Excel',
            'min_education': 'Undergraduate (BBA/B.Com/B.A. Advertising)',
            'salary_range': '₹3,00,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Stable',
            'higher_studies_options': 'Postgraduate in Media & Communication Management',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Advertising bases", "desc": "Understand media metrics like impressions, click rates, and target demographics."}, {"step": 2, "title": "Media Market Research", "desc": "Evaluate target audience reading/viewing habits using analytical databases."}, {"step": 3, "title": "Negotiate Media Rates", "desc": "Negotiate advertising rates with digital networks and television channels."}, {"step": 4, "title": "Media Spend Optimization", "desc": "Allocate campaign budgets across channels to maximize return on ad spend (ROAS)."}, {"step": 5, "title": "Campaign Tracking", "desc": "Monitor live click/impression metrics and adjust visual layouts mid-campaign."}])
        },
        {
            'title': 'Wealth Manager',
            'stream': 'Commerce/Management',
            'description': 'Provide high-net-worth clients with tailored investment, tax, retirement, and estate planning services.',
            'required_skills': 'Wealth Management, Investment Strategy, Tax Planning, Relationship Management, Excel',
            'min_education': 'Undergraduate (B.Com/BBA/B.Sc Finance) & CFP',
            'salary_range': '₹4,00,000 - ₹16,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'CFA Charter, MBA (Wealth Management/Finance)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Wealth Core", "desc": "Understand private banking, mutual fund structures, estate regulations, and global asset markets."}, {"step": 2, "title": "Client Relationship Skills", "desc": "Develop sales pitching and financial consulting skills."}, {"step": 3, "title": "Structured Asset Allocation", "desc": "Design diversified portfolios combining debt, equities, gold, and real estate."}, {"step": 4, "title": "Estate & Tax advisory", "desc": "Help clients structure trust funds, create wills, and organize tax write-offs."}, {"step": 5, "title": "Portfolio Optimization", "desc": "Track wealth performance and suggest asset rebalancing cycles."}])
        },
        {
            'title': 'UX Researcher',
            'stream': 'Design/Arts',
            'description': 'Conduct user interviews, run usability tests, and compile behavioral insights to guide UI design teams.',
            'required_skills': 'User Research, Usability Testing, Persona Creation, Information Architecture, Data Analysis',
            'min_education': 'Undergraduate (B.Des/B.A. Psychology/Humanities)',
            'salary_range': '₹4,00,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'M.Des in Interaction Design, HCI Certifications',
            'roadmap_steps': json.dumps([{"step": 1, "title": "HCI Principles", "desc": "Study Human-Computer Interaction, user psychology, and usability principles."}, {"step": 2, "title": "User Research Methods", "desc": "Learn to design surveys, run focus groups, and host user interviews."}, {"step": 3, "title": "Usability Testing", "desc": "Run testing sessions, record screen interactions, and build heatmaps."}, {"step": 4, "title": "Research Reports", "desc": "Draft user personas, journey maps, and list interface improvements."}, {"step": 5, "title": "Consult Design Team", "desc": "Share design suggestions with UI designers to guide wireframe updates."}])
        },
        {
            'title': 'Landscape Architect',
            'stream': 'Design/Arts',
            'description': 'Plan and design outdoor spaces like parks, gardens, recreational facilities, and urban landscape developments.',
            'required_skills': 'AutoCAD, Site Analysis, Landscape Design, Plant Selection, Spatial Planning, Revit',
            'min_education': 'Undergraduate (B.Arch/B.Des Landscape)',
            'salary_range': '₹3,50,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'Master of Landscape Architecture (MLA)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Landscape Architecture foundations", "desc": "Learn spatial drafting, soil dynamics, hydrology, and plant botany."}, {"step": 2, "title": "Design Software Mastery", "desc": "Learn AutoCAD, SketchUp, and specialized landscape modeling packages."}, {"step": 3, "title": "Site Grading & Drainage", "desc": "Draft site contour designs, drainage networks, and path layouts."}, {"step": 4, "title": "Plant Selection & Ecology", "desc": "Select trees and turf matching regional soils and climate targets."}, {"step": 5, "title": "Project Construction Site Supervision", "desc": "Supervise softscape planting and hardscape paving builds on site."}])
        },
        {
            'title': 'Visual Merchandiser',
            'stream': 'Design/Arts',
            'description': 'Design retail store window layouts, pick product display visual grids, and style showroom floor plans to drive purchases.',
            'required_skills': 'Visual Merchandising, Store Styling, Graphic Design, Brand Alignment, Spatial Display',
            'min_education': 'Undergraduate (B.Des/BFA/Diploma in Fashion Styling)',
            'salary_range': '₹2,50,000 - ₹8,50,000',
            'type': 'Private Sector',
            'difficulty': 'Easy',
            'market_demand': 'Stable',
            'higher_studies_options': 'Specialized courses in Luxury Retail Merchandising',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Design & Styling Basics", "desc": "Learn retail psychology, color theory, display grids, and lighting setups."}, {"step": 2, "title": "Window Display Concepts", "desc": "Draft creative seasonal mockup themes for showcase window frames."}, {"step": 3, "title": "Showroom Floor Planning", "desc": "Organize clothes racks, mannequins, and signage to guide customer foot traffic."}, {"step": 4, "title": "Display Materials Procurement", "desc": "Select acrylic models, print displays, and compile merchandising budgets."}, {"step": 5, "title": "Brand Presentation Audits", "desc": "Audit visual consistency across regional franchise stores."}])
        },
        {
            'title': 'Corporate Compliance Officer',
            'stream': 'Law',
            'description': 'Develop internal company policies, audit operating workflows, and ensure compliance with regional business laws.',
            'required_skills': 'Corporate Law, Compliance, Auditing, Policy Development, Risk Assessment, Legal Writing',
            'min_education': 'Undergraduate (LLB/BA-LLB/B.Com + CS)',
            'salary_range': '₹4,50,000 - ₹15,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'High',
            'higher_studies_options': 'Company Secretary (CS) certification, Post Graduate Diploma in Business Laws',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Corporate Law Core", "desc": "Study Companies Act, contract laws, labor codes, and market rules."}, {"step": 2, "title": "Internal Policy Auditing", "desc": "Learn corporate ethics codes, ESG parameters, and environmental regulations."}, {"step": 3, "title": "Risk Assessment Checks", "desc": "Perform audit checklists to discover regulatory vulnerabilities."}, {"step": 4, "title": "Filing Corporate Disclosures", "desc": "Prepare and file corporate audit disclosures to government boards."}, {"step": 5, "title": "Compliance Program Training", "desc": "Deliver internal compliance training workshops to employees."}])
        },
        {
            'title': 'Patent Agent',
            'stream': 'Law',
            'description': 'Draft patent specifications, search patent databases for novel inventions, and file agent responses to examiners.',
            'required_skills': 'Patent Drafting, Patent Searching, Patent Laws, Technical Writing, Scientific Analysis',
            'min_education': 'Undergraduate (B.Tech/B.Sc Science) & Patent Agent Registration',
            'salary_range': '₹4,00,000 - ₹14,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Growing',
            'higher_studies_options': 'LLB (Specializing in IP Law)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Science/Tech Education", "desc": "Earn a degree in engineering, physics, chemistry, or biological sciences."}, {"step": 2, "title": "Pass Patent Agent Exam", "desc": "Study Patents Act and pass the official Patent Agent Registration Exam."}, {"step": 3, "title": "Prior Art Searches", "desc": "Search databases like WIPO or USPTO to confirm the novelty of inventions."}, {"step": 4, "title": "Patent Claim Drafting", "desc": "Draft technical specifications detailing the scope of new patent protections."}, {"step": 5, "title": "Prosecution & Hearings", "desc": "Respond to official patent office objections and attend hearings."}])
        },
        {
            'title': 'Clinical Pharmacist',
            'stream': 'Medical/Pharmacy',
            'description': 'Collaborate with physicians in hospitals to select correct drug therapies, monitor patient doses, and counsel safety.',
            'required_skills': 'Clinical Pharmacy, Pharmacology, Dose Calculation, Drug Interactions, Patient Counseling',
            'min_education': 'Undergraduate (B.Pharm) / Pharm.D',
            'salary_range': '₹3,00,000 - ₹9,00,000',
            'type': 'Private Sector',
            'difficulty': 'Hard',
            'market_demand': 'Stable',
            'higher_studies_options': 'M.Pharm in Clinical Pharmacy, Ph.D. in Therapeutics',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Pharmacy bases", "desc": "Graduate with a B.Pharm or Doctor of Pharmacy (Pharm.D) degree."}, {"step": 2, "title": "Hospital Clinical Rotations", "desc": "Undergo hospital clinical training in medicine and surgical wards."}, {"step": 3, "title": "Calculate Drug Doses", "desc": "Calculate patient drug doses based on renal and hepatic functions."}, {"step": 4, "title": "Detect Drug Interactions", "desc": "Analyze patient chart lines to spot drug-drug or drug-food incompatibilities."}, {"step": 5, "title": "Patient Drug Safety Counseling", "desc": "Counsel discharging patients on correct drug intake schedules."}])
        },
        {
            'title': 'Healthcare Administrator',
            'stream': 'Medical/Pharmacy',
            'description': 'Coordinate daily operations, manage medical records systems, and oversee budgets in hospitals or clinic networks.',
            'required_skills': 'Healthcare Operations, Budgeting, Medical Billing, Regulatory Compliance, HR Management',
            'min_education': 'Undergraduate (B.Sc Healthcare/BHM/BBA)',
            'salary_range': '₹3,50,000 - ₹12,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Growing',
            'higher_studies_options': 'Master of Hospital Administration (MHA)',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Healthcare basics", "desc": "Understand medical terminologies, hospital organization divisions, and medical ethics."}, {"step": 2, "title": "Hospital Information Systems", "desc": "Learn to manage patient registration and EHR databases."}, {"step": 3, "title": "Medical Billing & Insurance", "desc": "Coordinate medical coding, pricing sheets, and insurance claims."}, {"step": 4, "title": "Hospital Staff Scheduling", "desc": "Schedule shift calendars for nursing teams and doctors."}, {"step": 5, "title": "Hospital Quality Certifications", "desc": "Prepare hospital departments for safety and hygiene audits."}])
        },
        {
            'title': 'Instructional Designer',
            'stream': 'Education/Humanities',
            'description': 'Design corporate online learning modules, write script storyboards, and build educational slides.',
            'required_skills': 'Instructional Design, Storyboarding, E-Learning Tools (Storyline), Bloom Taxonomy, Adult Learning',
            'min_education': 'Undergraduate (B.A. English/Humanities/B.Ed)',
            'salary_range': '₹3,50,000 - ₹10,00,000',
            'type': 'Private Sector',
            'difficulty': 'Medium',
            'market_demand': 'Stable',
            'higher_studies_options': 'Postgraduate in Instructional Design & Technology',
            'roadmap_steps': json.dumps([{"step": 1, "title": "Adult Learning Theory", "desc": "Study instructional frameworks like ADDIE, SAM, and adult learning traits."}, {"step": 2, "title": "Course Script Storyboarding", "desc": "Write visual scripts and dialogue prompts for educational designers."}, {"step": 3, "title": "Articulate Storyline tools", "desc": "Learn to compile interactive course files with triggers and quizzes."}, {"step": 4, "title": "Multimedia Integration", "desc": "Incorporate graphics, voiceovers, and videos into learning modules."}, {"step": 5, "title": "LMS Platform Management", "desc": "Upload course files and track student success metrics on platforms like Moodle."}])
        }
    ]
    
    # Check if Careers already exist, if not seed them
    if not Career.query.first():
        for c in careers_data:
            career = Career(**c)
            db.session.add(career)
        db.session.commit()

    # 3. Add Jobs (realistic job details for matching)
    jobs_data = [
        {
            'title': 'Junior Python Developer',
            'company': 'Tech Solutions Pvt Ltd',
            'description': 'Looking for a Junior Python developer to assist in building API microservices. You will write clean, documented code and collaborate on DB schemas.',
            'type': 'Full-Time',
            'location': 'Bangalore (Metro)',
            'skills_required': 'Python, SQL, Git, API, Data Structures',
            'salary': '₹5,00,000 - ₹7,00,000',
            'experience_required': 1.0,
            'link': 'https://example-jobs.com/python-dev'
        },
        {
            'title': 'Data Analyst Intern',
            'company': 'Global Analytics Corp',
            'description': 'Great opportunity for freshers to start a data career. Analyze spreadsheets, build visualizations, and query database setups.',
            'type': 'Internship',
            'location': 'Remote',
            'skills_required': 'SQL, Python, Excel, Data Visualization',
            'salary': '₹15,000 - ₹25,000 / month',
            'experience_required': 0.0,
            'link': 'https://example-jobs.com/data-intern'
        },
        {
            'title': 'Figma UX Designer',
            'company': 'Pixel Perfect Studio',
            'description': 'We need a contract UX designer to build mobile interface wireframes and complete responsive user prototypes on Figma.',
            'type': 'Freelance',
            'location': 'Remote',
            'skills_required': 'Figma, Prototyping, Wireframing, UX Design',
            'salary': '₹30,000 - ₹50,000 / project',
            'experience_required': 1.5,
            'link': 'https://example-jobs.com/freelance-ux'
        },
        {
            'title': 'Junior Tax Accountant',
            'company': 'Sharma & Associates CA',
            'description': 'Assist in filing business tax returns, compiling ledger books, and helping audit corporate financial statements.',
            'type': 'Full-Time',
            'location': 'Mumbai (Metro)',
            'skills_required': 'Taxation, Accounting, Excel, Auditing',
            'salary': '₹4,00,000 - ₹6,00,000',
            'experience_required': 0.0,
            'link': 'https://example-jobs.com/junior-ca'
        },
        {
            'title': 'Associate Site Engineer',
            'company': 'BuildSmart Builders',
            'description': 'Supervise daily construction execution, ensure safety compliance, verify drafts on AutoCAD, and count steel estimations.',
            'type': 'Full-Time',
            'location': 'Chennai (Non-Metro)',
            'skills_required': 'AutoCAD, Site Supervision, Estimation',
            'salary': '₹3,00,000 - ₹4,50,000',
            'experience_required': 1.0,
            'link': 'https://example-jobs.com/site-eng'
        },
        {
            'title': 'Retail Pharmacist',
            'company': 'MedStore Healthcare',
            'description': 'Handle medication distribution at our flagship pharmacy store. Review prescription accuracy and oversee pharmacy inventory.',
            'type': 'Full-Time',
            'location': 'Hyderabad (Metro)',
            'skills_required': 'Pharmacology, Customer Service, Inventory Management',
            'salary': '₹3,00,000 - ₹4,00,000',
            'experience_required': 0.0,
            'link': 'https://example-jobs.com/retail-pharmacist'
        }
    ]
    
    if not Job.query.first():
        for j in jobs_data:
            job = Job(**j)
            db.session.add(job)
        db.session.commit()

    # 4. Add Courses
    courses_data = [
        {'title': 'Python Coding Bootcamp', 'provider': 'Jose Portilla', 'platform': 'Udemy', 'skill_category': 'Python', 'difficulty': 'Beginner', 'duration': '22 hours', 'rating': 4.7, 'link': 'https://udemy.com/python-bootcamp'},
        {'title': 'Introduction to Data Structures & Algorithms', 'provider': 'UC San Diego', 'platform': 'Coursera', 'skill_category': 'Data Structures', 'difficulty': 'Intermediate', 'duration': '4 weeks', 'rating': 4.6, 'link': 'https://coursera.org/dsa'},
        {'title': 'Git and GitHub Crash Course', 'provider': 'Google', 'platform': 'Coursera', 'skill_category': 'Git', 'difficulty': 'Beginner', 'duration': '12 hours', 'rating': 4.8, 'link': 'https://coursera.org/git-google'},
        {'title': 'Machine Learning A-Z', 'provider': 'Kirill Eremenko', 'platform': 'Udemy', 'skill_category': 'Machine Learning', 'difficulty': 'Intermediate', 'duration': '40 hours', 'rating': 4.5, 'link': 'https://udemy.com/machine-learning'},
        {'title': 'Financial Accounting Standards', 'provider': 'IIT Madras', 'platform': 'NPTEL', 'skill_category': 'Accounting', 'difficulty': 'Beginner', 'duration': '8 weeks', 'rating': 4.4, 'link': 'https://nptel.ac.in/accounting'},
        {'title': 'Figma UI/UX Design Fundamentals', 'provider': 'Daniel Walter Scott', 'platform': 'Udemy', 'skill_category': 'Figma', 'difficulty': 'Beginner', 'duration': '10 hours', 'rating': 4.8, 'link': 'https://udemy.com/figma-design'},
        {'title': 'AutoCAD 2D Drafting & Design', 'provider': 'Autodesk Academy', 'platform': 'Coursera', 'skill_category': 'AutoCAD', 'difficulty': 'Beginner', 'duration': '6 weeks', 'rating': 4.5, 'link': 'https://coursera.org/autocad'},
        {'title': 'Clinical Research & Pharmacology Principles', 'provider': 'AIIMS Delhi', 'platform': 'NPTEL', 'skill_category': 'Pharmacology', 'difficulty': 'Intermediate', 'duration': '12 weeks', 'rating': 4.7, 'link': 'https://nptel.ac.in/pharmacology'}
    ]
    
    if not Course.query.first():
        for c in courses_data:
            course = Course(**c)
            db.session.add(course)
        db.session.commit()

        
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    with app.app_context():
        print("Dropping all database tables for schema refresh...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        # Seed content
        seed_database()
