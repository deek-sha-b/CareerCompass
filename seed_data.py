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
