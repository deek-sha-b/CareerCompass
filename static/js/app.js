// Core Application Controller - Career Guidance, Job Matcher & Resume Generator

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    App.init();
});

const App = {
    currentView: 'home',
    currentUser: null,
    
    init() {
        this.setupThemeToggle();
        this.setupAuthUI();
        this.setupNavigation();
        this.setupEventListeners();
        
        const appContainer = document.getElementById('app-container');
        
        if (Auth.isLoggedIn()) {
            if (appContainer) appContainer.classList.remove('landing-mode');
            this.handleLoginSuccess();
            const startView = Auth.getUserRole() === 'admin' ? 'admin' : 'dashboard';
            this.switchView(startView);
        } else {
            if (appContainer) appContainer.classList.add('landing-mode');
            this.switchView('home');
        }
        
        this.updateSidebarNavigation();
    },

    // ----------------- ROUTING & VIEW NAV -----------------
    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const view = e.currentTarget.getAttribute('data-view');
                if (view) {
                    this.switchView(view);
                }
            });
        });

        // Mobile Burger Menu
        const sidebar = document.querySelector('aside');
        const burger = document.getElementById('menu-burger');
        if (burger) {
            burger.addEventListener('click', () => {
                sidebar.classList.toggle('active');
            });
        }
    },

    switchView(viewId) {
        if (viewId === 'dashboard' && Auth.getUserRole() === 'admin') {
            viewId = 'admin';
        }
        this.currentView = viewId;
        
        // Update navigation active class
        document.querySelectorAll('.nav-item').forEach(item => {
            if (item.getAttribute('data-view') === viewId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        // Toggle view containers
        document.querySelectorAll('.view-section').forEach(section => {
            section.classList.remove('active');
        });
        
        const targetSection = document.getElementById(`view-${viewId}`);
        if (targetSection) {
            targetSection.classList.add('active');
            // Execute view load hook
            this.onViewLoaded(viewId);
        }
        
        // Close sidebar on mobile
        const sidebar = document.querySelector('aside');
        if (sidebar) sidebar.classList.remove('active');
    },

    onViewLoaded(viewId) {
        console.log(`Loaded view: ${viewId}`);
        if (viewId === 'dashboard') {
            this.loadDashboardData();
        } else if (viewId === 'careers') {
            const checkAndLoadRoadmap = async () => {
                if (!this.currentUser && Auth.isLoggedIn()) {
                    this.currentUser = await Auth.getProfile();
                }
                
                // Default the stream filter select dropdown to the user's stream
                const streamFilterSelect = document.getElementById('career-stream-filter');
                if (streamFilterSelect && this.currentUser && this.currentUser.stream) {
                    streamFilterSelect.value = this.currentUser.stream;
                }
                
                await this.loadCareersData();
                
                const roadmapCard = document.getElementById('career-roadmap-card');
                if (roadmapCard && roadmapCard.style.display !== 'block') {
                    if (this.currentUser && this.currentUser.target_goal) {
                        const targetGoal = this.currentUser.target_goal.toLowerCase().trim();
                        if (this.careersList) {
                            const matchingCareer = this.careersList.find(c => {
                                const title = c.title.toLowerCase().trim();
                                return title.includes(targetGoal) || targetGoal.includes(title);
                            });
                            if (matchingCareer) {
                                this.showRoadmap(matchingCareer.id);
                            }
                        }
                    }
                }
            };
            checkAndLoadRoadmap();
        } else if (viewId === 'jobs') {
            this.loadJobsData();
        } else if (viewId === 'resume') {
            this.loadResumeData();
        } else if (viewId === 'skills') {
            this.loadSkillsData();

        } else if (viewId === 'admin') {
            this.loadAdminData();
        }
    },

    // ----------------- DESIGN THEME SYSTEM -----------------
    setupThemeToggle() {
        const themeBtns = document.querySelectorAll('button[title="Toggle Theme"]');
        if (themeBtns.length === 0) return;
        
        // Set initial theme
        const savedTheme = localStorage.getItem('app_theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const updateButtons = (theme) => {
            themeBtns.forEach(btn => {
                btn.innerHTML = theme === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            });
        };
        updateButtons(savedTheme);
        
        themeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('app_theme', newTheme);
                updateButtons(newTheme);
                this.showNotification(`Theme switched to ${newTheme} mode!`, 'info');
            });
        });
    },

    // ----------------- TOAST NOTIFICATIONS -----------------
    showNotification(message, type = 'info') {
        const toast = document.getElementById('notification-toast');
        if (!toast) return;
        
        let icon = '<i class="fas fa-info-circle"></i>';
        if (type === 'success') icon = '<i class="fas fa-check-circle" style="color:var(--success-color)"></i>';
        if (type === 'warning') icon = '<i class="fas fa-exclamation-triangle" style="color:var(--warning-color)"></i>';
        if (type === 'danger') icon = '<i class="fas fa-times-circle" style="color:var(--danger-color)"></i>';
        
        toast.innerHTML = `${icon} <span>${message}</span>`;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    },

    // ----------------- AUTHENTICATION -----------------
    setupAuthUI() {
        const loginBtn = document.getElementById('btn-submit-login');
        const registerBtn = document.getElementById('btn-submit-register');
        const logoutBtn = document.getElementById('btn-logout');
        
        // Tab switching in login screen
        const tabLogin = document.getElementById('tab-login');
        const tabRegister = document.getElementById('tab-register');
        const formLogin = document.getElementById('form-login-fields');
        const formRegister = document.getElementById('form-register-fields');
        
        if (tabLogin && tabRegister) {
            tabLogin.addEventListener('click', () => {
                tabLogin.classList.add('active');
                tabRegister.classList.remove('active');
                formLogin.style.display = 'block';
                formRegister.style.display = 'none';
            });
            
            tabRegister.addEventListener('click', () => {
                tabRegister.classList.add('active');
                tabLogin.classList.remove('active');
                formRegister.style.display = 'block';
                formLogin.style.display = 'none';
            });
        }
        
        // Modal Open/Close triggers
        const authModal = document.getElementById('auth-modal');
        const closeAuthBtn = document.getElementById('btn-close-auth');
        const triggerBtns = [
            document.getElementById('btn-header-login'),
            document.getElementById('btn-hero-get-started'),
            document.getElementById('btn-footer-login')
        ];

        triggerBtns.forEach(btn => {
            if (btn) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (authModal) {
                        authModal.style.display = 'flex';
                    }
                });
            }
        });

        if (closeAuthBtn && authModal) {
            closeAuthBtn.addEventListener('click', () => {
                authModal.style.display = 'none';
            });
        }

        if (authModal) {
            authModal.addEventListener('click', (e) => {
                if (e.target === authModal) {
                    authModal.style.display = 'none';
                }
            });
        }
        
        if (loginBtn) {
            loginBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                const userVal = document.getElementById('login-username').value.trim();
                const passVal = document.getElementById('login-password').value;
                
                if (!userVal || !passVal) {
                    this.showNotification('Please fill all fields', 'warning');
                    return;
                }
                
                try {
                    await Auth.login(userVal, passVal);
                    this.showNotification('Welcome back!', 'success');
                    
                    if (authModal) authModal.style.display = 'none';
                    const appContainer = document.getElementById('app-container');
                    if (appContainer) appContainer.classList.remove('landing-mode');
                    
                    await this.handleLoginSuccess();
                    const startView = Auth.getUserRole() === 'admin' ? 'admin' : 'dashboard';
                    this.switchView(startView);
                } catch (err) {
                    this.showNotification(err.message, 'danger');
                }
            });
        }
        
        if (registerBtn) {
            registerBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                const userVal = document.getElementById('reg-username').value.trim();
                const emailVal = document.getElementById('reg-email').value.trim();
                const passVal = document.getElementById('reg-password').value;
                
                if (!userVal || !emailVal || !passVal) {
                    this.showNotification('Please fill all fields', 'warning');
                    return;
                }
                
                try {
                    await Auth.register(userVal, emailVal, passVal, 'student');
                    this.showNotification('Registration successful! Please login.', 'success');
                    tabLogin.click();
                } catch (err) {
                    this.showNotification(err.message, 'danger');
                }
            });
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                Auth.clearToken();
                this.currentUser = null;
                
                const appContainer = document.getElementById('app-container');
                if (appContainer) appContainer.classList.add('landing-mode');
                
                this.updateSidebarNavigation();
                this.switchView('home');
                
                this.showNotification('Logged out successfully', 'success');
            });
        }
    },

    async handleLoginSuccess() {
        document.getElementById('nav-user-box').style.display = 'flex';
        document.getElementById('username-display').innerText = Auth.getUsername();
        document.getElementById('user-role-display').innerText = Auth.getUserRole().toUpperCase();
        
        // Show admin nav link if appropriate
        if (Auth.getUserRole() === 'admin') {
            document.getElementById('nav-admin').style.display = 'flex';
        } else {
            document.getElementById('nav-admin').style.display = 'none';
        }
        
        // Update sidebar links based on role
        this.updateSidebarNavigation();
        
        // Load profile data into app cache
        this.currentUser = await Auth.getProfile();
    },

    isProfileValid(prof) {
        if (!prof) return false;
        const stream = (prof.stream || '').trim();
        const qualification = (prof.qualification || '').trim();
        const target_goal = (prof.target_goal || '').trim();
        
        const skills = Array.isArray(prof.current_skills) ? prof.current_skills : 
                       (typeof prof.current_skills === 'string' ? prof.current_skills.split(',') : []);
        const cleanSkills = skills.map(s => s.trim()).filter(s => s.length > 0);
        
        const interests = Array.isArray(prof.interests) ? prof.interests : 
                          (typeof prof.interests === 'string' ? prof.interests.split(',') : []);
        const cleanInterests = interests.map(i => i.trim()).filter(i => i.length > 0);
        
        return !!(stream && qualification && target_goal && cleanSkills.length > 0 && cleanInterests.length > 0);
    },

    getStreamUiName(stream) {
        if (!stream) return "Not Selected";
        const s = stream.toLowerCase();
        if (s.includes('hotel') || s.includes('vocational')) {
            return "Hospitality & Vocational";
        } else if (s.includes('engineering') || s.includes('technology') || s.includes('computer') || s.includes('science')) {
            return "Computer Science / IT";
        } else if (s.includes('commerce') || s.includes('management')) {
            return "Commerce / Management";
        } else if (s.includes('design') || s.includes('art')) {
            return "Design / Arts";
        } else if (s.includes('law')) {
            return "Law";
        } else if (s.includes('medical') || s.includes('pharmacy')) {
            return "Medical / Pharmacy";
        } else if (s.includes('education') || s.includes('humanities')) {
            return "Humanities / Arts";
        } else {
            return stream;
        }
    },

    calculateCompletion(profile, isValidated, isValidationError) {
        if (isValidationError || !profile) {
            return 0;
        }
        
        const stream = (profile.stream || '').trim();
        const qualification = (profile.qualification || '').trim();
        const target_goal = (profile.target_goal || '').trim();
        
        const skills = Array.isArray(profile.current_skills) ? profile.current_skills : 
                       (typeof profile.current_skills === 'string' ? profile.current_skills.split(',') : []);
        const cleanSkills = skills.map(s => s.trim()).filter(s => s.length > 0);
        
        const interests = Array.isArray(profile.interests) ? profile.interests : 
                          (typeof profile.interests === 'string' ? profile.interests.split(',') : []);
        const cleanInterests = interests.map(i => i.trim()).filter(i => i.length > 0);
        
        let filledCount = 0;
        if ((profile.full_name || '').trim()) filledCount++;
        if (profile.age && parseInt(profile.age) > 0) filledCount++;
        if (stream) filledCount++;
        if (qualification) filledCount++;
        if (cleanSkills.length > 0) filledCount++;
        if (cleanInterests.length > 0) filledCount++;
        if ((profile.academic_performance || '').trim()) filledCount++;
        if (target_goal) filledCount++;
        if (profile.experience_years !== undefined && profile.experience_years !== null && parseFloat(profile.experience_years) > 0) filledCount++;
        if ((profile.bio || '').trim()) filledCount++;
        
        if (filledCount === 0) {
            return 0;
        }
        
        const isCurrentlyValid = stream && qualification && target_goal && cleanSkills.length > 0 && cleanInterests.length > 0;
        
        if (isValidated && isCurrentlyValid) {
            return Math.round((filledCount / 10) * 100);
        } else {
            if (!stream) {
                return 0;
            } else {
                return Math.min(60, Math.max(20, Math.round((filledCount / 10) * 100)));
            }
        }
    },

    // ----------------- STUDENT DASHBOARD -----------------
    async loadDashboardData() {
        try {
            // Load profile metrics
            const profile = await Auth.getProfile();
            this.currentUser = profile;
            
            if (profile) {
                const isValid = this.isProfileValid(profile);
                const completionVal = this.calculateCompletion(profile, isValid, false);
                document.getElementById('profile-completion').innerText = `${completionVal}%`;
                
                // Show core user stream and qualification info
                const streamDisplay = isValid ? this.getStreamUiName(profile.stream) : 'Not Selected';
                document.getElementById('dash-stream').innerText = streamDisplay;
                const dashQual = document.getElementById('dash-qualification');
                if (dashQual) {
                    dashQual.innerText = profile.qualification || 'Not Set';
                }
                
                // Fill details inputs
                document.getElementById('profile-name').value = profile.full_name || '';
                document.getElementById('profile-age').value = profile.age || '';
                document.getElementById('profile-stream-select').value = profile.stream || '';
                document.getElementById('profile-qual-select').value = profile.qualification || '';
                document.getElementById('profile-skills').value = profile.current_skills.join(', ');
                document.getElementById('profile-interests').value = profile.interests.join(', ');
                document.getElementById('profile-academic').value = profile.academic_performance || '';
                document.getElementById('profile-goal').value = profile.target_goal || '';
                document.getElementById('profile-experience').value = profile.experience_years || 0;
                document.getElementById('profile-bio').value = profile.bio || '';
            }
            
            // Clear recommendations to initial state on load / refresh
            const container = document.getElementById('dash-careers-preview');
            if (container) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 30px 20px;">
                        <h3 style="color:var(--text-secondary); font-size:16px; margin-bottom:12px;"><i class="fa-solid fa-triangle-exclamation"></i> No Recommendations Available</h3>
                        <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom: 8px;">Complete and validate your profile to receive personalized career recommendations.</p>
                        <div style="border-top: 1px dashed var(--card-border); margin: 16px 0; padding-top: 12px;">
                            <p style="font-size:12px; color:var(--text-muted); margin-bottom: 4px;">No recommendations yet.</p>
                            <p style="font-size:12px; color:var(--text-muted); margin-bottom: 4px;">Fill out your profile and click Save Profile.</p>
                            <span style="font-size:11px; color:var(--text-muted); display:block; margin-top:8px;">Recommendations will be generated after successful profile validation.</span>
                        </div>
                    </div>
                `;
            }
            
            // Load bookmarked jobs
            const savedJobsResponse = await fetch('/api/jobs/bookmark', { headers: Auth.getAuthHeaders() });
            if (savedJobsResponse.ok) {
                const jobs = await savedJobsResponse.json();
                document.getElementById('dash-saved-jobs-count').innerText = jobs.length;
            }
            
            
        } catch (err) {
            console.error('Error loading dashboard data:', err);
        }
    },

    async saveProfileData() {
        const stream = document.getElementById('profile-stream-select').value;
        const qualification = document.getElementById('profile-qual-select').value;
        const skillsRaw = document.getElementById('profile-skills').value.trim();
        const interestsRaw = document.getElementById('profile-interests').value.trim();
        const goal = document.getElementById('profile-goal').value.trim();
        
        const container = document.getElementById('dash-careers-preview');

        // Client-side quick check
        if (!stream || !qualification || !skillsRaw || !interestsRaw || !goal) {
            this.showNotification('Profile Validation Failed', 'danger');
            document.getElementById('profile-completion').innerText = '0%';
            document.getElementById('dash-stream').innerText = 'Not Selected';
            if (container) {
                container.innerHTML = `
                    <div class="glass-card" style="padding: 24px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.04); border-radius: 16px;">
                        <h3 style="color:#ef4444; font-size:16px; margin-bottom:12px;"><i class="fa-solid fa-circle-xmark"></i> Profile Validation Failed</h3>
                        <p style="font-weight:600; color:var(--text-primary); font-size:14px; margin-bottom:8px;">❌ Profile Validation Failed</p>
                        <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom:8px;">The entered education, skills, qualifications, and career goal do not match.</p>
                        <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">Please correct the information and try again.</p>
                        <span style="font-size:11px; color:#ef4444; font-weight:500;">No recommendations generated</span>
                    </div>
                `;
            }
            return;
        }

        const profileData = {
            full_name: document.getElementById('profile-name').value.trim(),
            age: parseInt(document.getElementById('profile-age').value) || null,
            stream: stream,
            qualification: qualification,
            current_skills: skillsRaw.split(',').map(s => s.trim()).filter(s => s.length > 0),
            interests: interestsRaw.split(',').map(s => s.trim()).filter(s => s.length > 0),
            academic_performance: document.getElementById('profile-academic').value.trim(),
            target_goal: goal,
            experience_years: parseFloat(document.getElementById('profile-experience').value) || 0.0,
            bio: document.getElementById('profile-bio').value.trim()
        };
        
        try {
            const result = await Auth.updateProfile(profileData);
            
            if (result && result.status === 'validation_failed') {
                this.showNotification(result.message || 'Profile Validation Failed', 'danger');
                document.getElementById('profile-completion').innerText = '0%';
                document.getElementById('dash-stream').innerText = 'Not Selected';
                if (container) {
                    if (result.suggested_actions && result.suggested_actions.length > 0) {
                        const actionsHtml = result.suggested_actions.map(a => `<li>${a}</li>`).join('');
                        container.innerHTML = `
                            <div class="glass-card" style="padding: 24px; text-align: left; border: 1.5px solid var(--warning-color); background: rgba(255, 193, 7, 0.04); border-radius: 16px;">
                                <h3 style="color:var(--warning-color); font-size:17px; font-weight:700; margin-bottom:12px; text-align:center;">
                                    <i class="fa-solid fa-circle-exclamation" style="margin-right:6px;"></i>${result.message || 'Insufficient Data Match'}
                                </h3>
                                <p style="font-size:14px; color:var(--text-primary); line-height:1.6; margin-bottom:16px; font-weight:500;">
                                    ${result.warning_details || 'The entered education, skills, qualifications, and career goal do not match.'}
                                </p>
                                <div style="border-top: 1px dashed rgba(255, 193, 7, 0.2); margin-top: 16px; padding-top: 16px;">
                                    <strong style="color:var(--warning-color); font-size:13px; display:block; margin-bottom:8px;">Suggested Actions:</strong>
                                    <ul style="padding-left:20px; font-size:13px; color:var(--text-secondary); line-height:1.6;">
                                        ${actionsHtml}
                                    </ul>
                                </div>
                            </div>
                        `;
                    } else {
                        container.innerHTML = `
                            <div class="glass-card" style="padding: 24px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.04); border-radius: 16px;">
                                <h3 style="color:#ef4444; font-size:16px; margin-bottom:12px;"><i class="fa-solid fa-circle-xmark"></i> Profile Validation Failed</h3>
                                <p style="font-weight:600; color:var(--text-primary); font-size:14px; margin-bottom:8px;">❌ Profile Validation Failed</p>
                                <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom:8px;">The entered education, skills, qualifications, and career goal do not match.</p>
                                <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">Please correct the information and try again.</p>
                                <span style="font-size:11px; color:#ef4444; font-weight:500;">No recommendations generated</span>
                            </div>
                        `;
                    }
                }
                return;
            }

            this.showNotification('Profile updated successfully!', 'success');
            
            // Update UI dashboard stats cards
            if (result && result.profile) {
                const profile = result.profile;
                this.currentUser = profile;
                const completionVal = this.calculateCompletion(profile, true, false);
                document.getElementById('profile-completion').innerText = `${completionVal}%`;
                document.getElementById('dash-stream').innerText = this.getStreamUiName(profile.stream);
                const dashQual = document.getElementById('dash-qualification');
                if (dashQual) {
                    dashQual.innerText = profile.qualification || 'Not Set';
                }
            }

            // Render recommendations
            if (result && Array.isArray(result.recommendations)) {
                this.renderRecommendations(result.recommendations);
            }
        } catch (err) {
            const result = err.response || {};
            this.showNotification(result.message || 'Profile Validation Failed', 'danger');
            document.getElementById('profile-completion').innerText = '0%';
            document.getElementById('dash-stream').innerText = 'Not Selected';
            if (container) {
                if (result.suggested_actions && result.suggested_actions.length > 0) {
                    const actionsHtml = result.suggested_actions.map(a => `<li>${a}</li>`).join('');
                    container.innerHTML = `
                        <div class="glass-card" style="padding: 24px; text-align: left; border: 1.5px solid var(--warning-color); background: rgba(255, 193, 7, 0.04); border-radius: 16px;">
                            <h3 style="color:var(--warning-color); font-size:17px; font-weight:700; margin-bottom:12px; text-align:center;">
                                <i class="fa-solid fa-circle-exclamation" style="margin-right:6px;"></i>${result.message || 'Insufficient Data Match'}
                            </h3>
                            <p style="font-size:14px; color:var(--text-primary); line-height:1.6; margin-bottom:16px; font-weight:500;">
                                ${result.warning_details || 'The entered education, skills, qualifications, and career goal do not match.'}
                            </p>
                            <div style="border-top: 1px dashed rgba(255, 193, 7, 0.2); margin-top: 16px; padding-top: 16px;">
                                <strong style="color:var(--warning-color); font-size:13px; display:block; margin-bottom:8px;">Suggested Actions:</strong>
                                <ul style="padding-left:20px; font-size:13px; color:var(--text-secondary); line-height:1.6;">
                                    ${actionsHtml}
                                </ul>
                            </div>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="glass-card" style="padding: 24px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.04); border-radius: 16px;">
                            <h3 style="color:#ef4444; font-size:16px; margin-bottom:12px;"><i class="fa-solid fa-circle-xmark"></i> Profile Validation Failed</h3>
                            <p style="font-weight:600; color:var(--text-primary); font-size:14px; margin-bottom:8px;">❌ Profile Validation Failed</p>
                            <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom:8px;">${result.message || 'The entered education, skills, qualifications, and career goal do not match.'}</p>
                            <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">Please correct the information and try again.</p>
                            <span style="font-size:11px; color:#ef4444; font-weight:500;">No recommendations generated</span>
                        </div>
                    `;
                }
            }
        }
    },

    renderRecommendations(recs) {
        const container = document.getElementById('dash-careers-preview');
        if (!container) return;
        
        if (!Array.isArray(recs) || recs.length === 0) {
            container.innerHTML = '<p class="text-muted">No matching careers found. Please update your profile settings!</p>';
            return;
        }
        
        container.innerHTML = '<p style="font-size:14px; color:var(--text-secondary); margin-bottom:16px;">Based on your qualifications and goals, our matching model highlights these tracks:</p>';
        
        recs.slice(0, 3).forEach(c => {
            const higherStudies = Array.isArray(c.higher_studies_options) && c.higher_studies_options.length > 0 
                ? c.higher_studies_options.join(', ') 
                : 'N/A';
                
            const courseLinks = Array.isArray(c.recommended_courses) && c.recommended_courses.length > 0
                ? c.recommended_courses.map(co => {
                    const escapedCourse = JSON.stringify(co).replace(/"/g, '&quot;');
                    return `<span class="suggested-course-item" onclick="App.showCourseDetails(${escapedCourse})" style="color:var(--accent-secondary); text-decoration:none; border-bottom:1px dashed var(--accent-secondary); cursor:pointer; font-weight:500;">${co.title} (${co.platform})</span>`;
                  }).join(', ')
                : 'N/A';
                
            let nextStepDesc = 'Begin core learning paths.';
            if (Array.isArray(c.roadmap_steps) && c.roadmap_steps.length > 0) {
                let stepObj = c.roadmap_steps[0];
                const hasDegree = ['Undergraduate', 'Postgraduate', 'Research/PhD', 'Working Professional'].includes(this.currentUser ? this.currentUser.qualification : '');
                if (hasDegree && c.roadmap_steps.length > 1 && 
                    (stepObj.title.toLowerCase().includes('degree') || 
                     stepObj.title.toLowerCase().includes('education') || 
                     stepObj.title.toLowerCase().includes('register') || 
                     stepObj.title.toLowerCase().includes('qualification') || 
                     stepObj.title.toLowerCase().includes('academic'))) {
                    stepObj = c.roadmap_steps[1];
                }
                nextStepDesc = `<strong>${stepObj.title}</strong>: ${stepObj.desc}`;
            }

            container.innerHTML += `
                <div class="glass-card" style="padding: 20px; margin-bottom: 16px; border-left: 4px solid var(--accent-primary);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">
                        <div>
                            <h4 style="color:var(--text-primary); font-size:15px; font-weight:600;">${c.title}</h4>
                            <span style="font-size:12px; color:var(--text-muted)">${c.stream}</span>
                        </div>
                        <span class="badge" style="background:var(--accent-primary); color:white; padding:4px 10px; border-radius:10px; font-size:11px; font-weight:600;">${c.match_score}% Match</span>
                    </div>
                    <div style="margin-top: 12px; display:flex; flex-direction:column; gap:8px; font-size:13px; text-align:left;">
                        <div>
                            <strong style="color:var(--text-secondary);"><i class="fa-solid fa-graduation-cap"></i> Higher Studies:</strong> 
                            <span style="color:var(--text-primary);">${higherStudies}</span>
                        </div>
                        <div>
                            <strong style="color:var(--text-secondary);"><i class="fa-solid fa-briefcase"></i> Job Entrance:</strong> 
                            <span style="color:var(--text-primary);">${c.min_education}</span>
                        </div>
                        <div>
                            <strong style="color:var(--text-secondary);"><i class="fa-solid fa-book-open"></i> Suggested Course:</strong> 
                            <span style="color:var(--text-primary);">${courseLinks}</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:8px; border:1px solid var(--card-border); margin-top:4px;">
                            <strong style="color:var(--accent-secondary); font-size:12px;"><i class="fa-solid fa-arrow-right-long"></i> Next Immediate Action:</strong>
                            <p style="color:var(--text-primary); font-size:12px; margin-top:4px; line-height:1.4;">${nextStepDesc}</p>
                        </div>
                    </div>
                </div>
            `;
        });
    },

    // ----------------- CAREERS & ROADMAPS -----------------
    async loadCareersData() {
        try {
            const searchVal = document.getElementById('career-search').value;
            const streamVal = document.getElementById('career-stream-filter').value;
            
            let url = '/api/careers/list';
            const params = [];
            if (searchVal) params.push(`search=${encodeURIComponent(searchVal)}`);
            if (streamVal) params.push(`stream=${encodeURIComponent(streamVal)}`);
            if (params.length > 0) url += '?' + params.join('&');
            
            const response = await fetch(url);
            const careers = await response.json();
            this.careersList = careers;
            
            // Get bookmarked careers
            const bookmarkedResponse = await fetch('/api/careers/bookmark', { headers: Auth.getAuthHeaders() });
            const bookmarked = bookmarkedResponse.ok ? await bookmarkedResponse.json() : [];
            const bookmarkedIds = bookmarked.map(b => b.id);
            
            const container = document.getElementById('careers-grid-container');
            container.innerHTML = '';
            
            if (careers.length === 0) {
                container.innerHTML = '<p class="text-muted" style="grid-column: 1/-1; text-align:center;">No career paths found. Try clearing filters.</p>';
                return;
            }
            
            careers.forEach(c => {
                const isBookmarked = bookmarkedIds.includes(c.id);
                container.innerHTML += `
                    <div class="glass-card glow-purple" style="padding-bottom: 70px;">
                        <span class="bookmark-badge ${isBookmarked ? 'active' : ''}" onclick="App.toggleCareerBookmark(${c.id})">
                            <i class="${isBookmarked ? 'fas' : 'far'} fa-bookmark"></i>
                        </span>
                        <h3 style="margin-bottom: 8px;">${c.title}</h3>
                        <span style="font-size:12px; color:var(--accent-secondary); background:rgba(0, 245, 255, 0.08); padding:4px 10px; border-radius:8px; display:inline-block; margin-bottom:12px;">${c.stream}</span>
                        <p style="font-size:14px; color:var(--text-secondary); margin-bottom:16px; min-height: 60px;">${c.description}</p>
                        
                        <div style="font-size:13px; margin-bottom:8px;">
                            <strong>Expected Salary:</strong> <span style="color:var(--success-color)">${c.salary_range}</span>
                        </div>
                        <div style="font-size:13px; margin-bottom:8px;">
                            <strong>Demand:</strong> <span style="color:var(--accent-secondary)">${c.market_demand}</span>
                        </div>
                        <div style="font-size:13px; margin-bottom:16px;">
                            <strong>Difficulty:</strong> <span>${c.difficulty}</span>
                        </div>
                        
                        <div style="position: absolute; bottom: 20px; left: 24px; right: 24px; display:flex; gap:10px;">
                            <button class="btn btn-primary" style="flex-grow: 1; padding: 8px 12px; font-size:13px;" onclick="App.showRoadmap(${c.id})">
                                <i class="fas fa-route"></i> Roadmap
                            </button>
                            <button class="btn btn-secondary" style="padding: 8px 12px;" onclick="App.addCompare(${c.id}, '${c.title}')" title="Compare Career">
                                <i class="fas fa-balance-scale"></i>
                            </button>
                        </div>
                    </div>
                `;
            });
            
            // Populating career comparative options
            const compareSelect1 = document.getElementById('compare-career-1');
            const compareSelect2 = document.getElementById('compare-career-2');
            if (compareSelect1 && compareSelect2) {
                compareSelect1.innerHTML = '<option value="">Select Career 1</option>';
                compareSelect2.innerHTML = '<option value="">Select Career 2</option>';
                careers.forEach(c => {
                    compareSelect1.innerHTML += `<option value="${c.id}">${c.title}</option>`;
                    compareSelect2.innerHTML += `<option value="${c.id}">${c.title}</option>`;
                });
            }
            
        } catch (err) {
            console.error('Error loading careers:', err);
        }
    },

    async toggleCareerBookmark(careerId) {
        try {
            const res = await fetch('/api/careers/bookmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeaders() },
                body: JSON.stringify({ career_id: careerId })
            });
            const data = await res.json();
            this.showNotification(data.message, 'success');
            this.loadCareersData();
            this.loadDashboardData();
        } catch (err) {
            this.showNotification(err.message, 'danger');
        }
    },

    async showRoadmap(careerId) {
        try {
            const res = await fetch(`/api/careers/roadmap/${careerId}`);
            const data = await res.json();
            
            const timeline = document.getElementById('roadmap-timeline-box');
            timeline.innerHTML = '';
            
            document.getElementById('roadmap-career-title').innerText = data.career_title;
            
            const qual = this.currentUser ? this.currentUser.qualification : '';
            const userSkills = this.currentUser && this.currentUser.current_skills ? 
                               (Array.isArray(this.currentUser.current_skills) ? this.currentUser.current_skills : 
                               (typeof this.currentUser.current_skills === 'string' ? this.currentUser.current_skills.split(',') : [])) : [];
            const cleanUserSkills = userSkills.map(s => s.trim().toLowerCase()).filter(s => s.length > 0);
            
            const hasDiploma = ['Diploma', 'Undergraduate', 'Postgraduate', 'Research/PhD', 'Working Professional'].includes(qual);
            const hasUndergrad = ['Undergraduate', 'Postgraduate', 'Research/PhD', 'Working Professional'].includes(qual);
            const hasPostgrad = ['Postgraduate', 'Research/PhD', 'Working Professional'].includes(qual);
            const hasPhD = ['Research/PhD', 'Working Professional'].includes(qual);
            const isProfessional = ['Working Professional'].includes(qual);
            
            // Determine the status for each step
            const stepsStatus = data.roadmap_steps.map((step, idx) => {
                const title = step.title.toLowerCase();
                const desc = step.desc.toLowerCase();
                
                // 1. Skill Match Check: If the user already has the skill(s) that this step focuses on, mark as completed
                const skillMatch = cleanUserSkills.some(skill => {
                    const hasSpecial = /[^a-z0-9_]/i.test(skill);
                    if (hasSpecial) {
                        return title.includes(skill) || desc.includes(skill);
                    } else {
                        const escaped = skill.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
                        const regex = new RegExp('\\b' + escaped + '\\b', 'i');
                        return regex.test(title) || regex.test(desc);
                    }
                });
                
                if (skillMatch) {
                    return 'completed';
                }
                
                // 2. Academic/Professional Qualification Match Check
                if (isProfessional) {
                    if (title.includes('degree') || title.includes('bachelor') || title.includes('undergraduate') || 
                        title.includes('master') || title.includes('postgraduate') || title.includes('phd') || 
                        title.includes('school') || title.includes('education') || title.includes('college') ||
                        title.includes('internship') || title.includes('articleship') || title.includes('training') ||
                        desc.includes('degree') || desc.includes('internship') || desc.includes('articleship') || desc.includes('training')) {
                        return 'completed';
                    }
                }
                
                if (hasPhD) {
                    if (title.includes('ph.d') || title.includes('phd') || title.includes('research') || title.includes('doctoral') || desc.includes('ph.d') || desc.includes('phd') || desc.includes('research') || desc.includes('doctoral')) {
                        return 'completed';
                    }
                }
                
                if (hasPostgrad) {
                    if (title.includes('master') || title.includes('postgraduate') || title.includes('mba') || title.includes('m.tech') || title.includes('m.sc') || title.includes('m.pharm') || title.includes('llm') || title.includes('pass intermediate exam') || desc.includes('master\'s degree') || desc.includes('postgraduate degree')) {
                        return 'completed';
                    }
                }
                
                if (hasUndergrad) {
                    if (title.includes('degree') || title.includes('bachelor') || title.includes('undergraduate') || title.includes('college') || title.includes('b.tech') || title.includes('b.e') || title.includes('bca') || title.includes('b.sc') || title.includes('b.com') || title.includes('bba') || title.includes('llb') || title.includes('ba-llb') || title.includes('b.pharm') || title.includes('d.pharm') || title.includes('academic degree') || title.includes('earn pharmacy qualification') || title.includes('law degree') || title.includes('agriculture education') || desc.includes('bachelor\'s degree') || desc.includes('undergraduate degree')) {
                        return 'completed';
                    }
                }
                
                if (hasDiploma) {
                    if (title.includes('diploma') || title.includes('polytechnic') || desc.includes('diploma') || desc.includes('polytechnic')) {
                        return 'completed';
                    }
                }
                
                if (qual && (title.includes('school') || title.includes('higher secondary') || title.includes('12th') || title.includes('register with icai') || desc.includes('school') || desc.includes('higher secondary') || desc.includes('12th'))) {
                    return 'completed';
                }
                
                return 'pending';
            });
            
            // Find the first index that is still 'pending' to mark as the 'active' focus
            let firstActiveIdx = stepsStatus.indexOf('pending');
            if (firstActiveIdx === -1) {
                firstActiveIdx = data.roadmap_steps.length - 1;
            }
            
            data.roadmap_steps.forEach((step, idx) => {
                let statusClass = stepsStatus[idx];
                if (idx === firstActiveIdx) {
                    statusClass = 'active';
                }
                
                let statusText = '';
                if (statusClass === 'completed') {
                    statusText = ' <span class="badge" style="background:var(--success-color); color:white; font-size:10px; padding:2px 6px; border-radius:4px; margin-left:8px;"><i class="fa-solid fa-check"></i> Completed</span>';
                } else if (statusClass === 'active') {
                    statusText = ' <span class="badge" style="background:var(--accent-primary); color:white; font-size:10px; padding:2px 6px; border-radius:4px; margin-left:8px;">Active Focus</span>';
                }
                
                timeline.innerHTML += `
                    <div class="roadmap-node ${statusClass}">
                        <div class="roadmap-dot"></div>
                        <div class="roadmap-content">
                            <h4 style="color:var(--text-primary)">Step ${step.step}: ${step.title}${statusText}</h4>
                            <p style="font-size:13px; color:var(--text-secondary); margin-top:6px;">${step.desc}</p>
                        </div>
                    </div>
                `;
            });
            
            // Slide in or trigger CSS display for roadmap card
            document.getElementById('career-roadmap-card').style.display = 'block';
            document.getElementById('career-roadmap-card').scrollIntoView({ behavior: 'smooth' });
            
        } catch (err) {
            console.error('Error fetching roadmap:', err);
        }
    },

    addCompare(careerId, careerTitle) {
        const c1 = document.getElementById('compare-career-1');
        const c2 = document.getElementById('compare-career-2');
        if (!c1.value) {
            c1.value = careerId;
        } else if (!c2.value && c1.value != careerId) {
            c2.value = careerId;
        } else {
            c1.value = careerId;
        }
        this.showNotification(`Added ${careerTitle} to comparison dashboard`, 'info');
        document.getElementById('comparison-box-card').scrollIntoView({ behavior: 'smooth' });
    },

    async runComparison() {
        const c1Val = document.getElementById('compare-career-1').value;
        const c2Val = document.getElementById('compare-career-2').value;
        
        if (!c1Val || !c2Val) {
            this.showNotification('Please select two career paths to compare', 'warning');
            return;
        }
        
        try {
            const res = await fetch('/api/careers/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ career_id_1: c1Val, career_id_2: c2Val })
            });
            const data = await res.json();
            
            const results = document.getElementById('comparison-results-box');
            results.innerHTML = `
                <div class="grid-2" style="margin-top: 20px;">
                    <div class="glass-card" style="border-color: var(--accent-primary)">
                        <h3>${data.career_1.title}</h3>
                        <p style="font-size:13px; color:var(--text-secondary); margin-top:8px;">${data.career_1.description}</p>
                        <ul style="margin-top:16px; font-size:13px; list-style:none; display:flex; flex-direction:column; gap:8px;">
                            <li><strong>Salary:</strong> ${data.career_1.salary_range}</li>
                            <li><strong>Demand:</strong> ${data.career_1.market_demand}</li>
                            <li><strong>Difficulty:</strong> ${data.career_1.difficulty}</li>
                            <li><strong>Min Education:</strong> ${data.career_1.min_education}</li>
                            <li><strong>Required Skills:</strong> ${data.career_1.required_skills.join(', ')}</li>
                        </ul>
                    </div>
                    <div class="glass-card" style="border-color: var(--accent-secondary)">
                        <h3>${data.career_2.title}</h3>
                        <p style="font-size:13px; color:var(--text-secondary); margin-top:8px;">${data.career_2.description}</p>
                        <ul style="margin-top:16px; font-size:13px; list-style:none; display:flex; flex-direction:column; gap:8px;">
                            <li><strong>Salary:</strong> ${data.career_2.salary_range}</li>
                            <li><strong>Demand:</strong> ${data.career_2.market_demand}</li>
                            <li><strong>Difficulty:</strong> ${data.career_2.difficulty}</li>
                            <li><strong>Min Education:</strong> ${data.career_2.min_education}</li>
                            <li><strong>Required Skills:</strong> ${data.career_2.required_skills.join(', ')}</li>
                        </ul>
                    </div>
                </div>
            `;
        } catch (err) {
            console.error('Comparison error:', err);
        }
    },

    // ----------------- JOB RECOMMENDATIONS -----------------
    async loadJobsData() {
        try {
            const searchVal = document.getElementById('job-search-input').value;
            const typeVal = document.getElementById('job-type-filter').value;
            const locationVal = document.getElementById('job-location-input').value;
            const toggleRec = document.getElementById('job-ai-recommend-toggle').checked;
            
            let url = '/api/jobs/list';
            if (toggleRec) {
                url = '/api/jobs/recommend';
            }
            
            const params = [];
            if (!toggleRec) {
                if (searchVal) params.push(`search=${encodeURIComponent(searchVal)}`);
                if (typeVal) params.push(`type=${encodeURIComponent(typeVal)}`);
                if (locationVal) params.push(`location=${encodeURIComponent(locationVal)}`);
                if (params.length > 0) url += '?' + params.join('&');
            }
            
            const res = await fetch(url, { headers: Auth.getAuthHeaders() });
            const jobs = await res.json();
            
            // Get bookmarked list
            const bookmarksRes = await fetch('/api/jobs/bookmark', { headers: Auth.getAuthHeaders() });
            const bookmarks = bookmarksRes.ok ? await bookmarksRes.json() : [];
            const bookmarkIds = bookmarks.map(b => b.id);
            
            const container = document.getElementById('jobs-listings-container');
            container.innerHTML = '';
            
            if (jobs.length === 0) {
                container.innerHTML = '<p class="text-muted" style="text-align:center; padding: 20px 0;">No matching jobs found. Try adjusting filters.</p>';
                return;
            }
            
            jobs.forEach(j => {
                const isBookmarked = bookmarkIds.includes(j.id);
                const scoreBadge = j.match_score ? 
                    `<span class="badge" style="background:var(--accent-secondary); color:#000; padding:6px 12px; border-radius:12px; font-weight:600; font-size:12px;">AI Score: ${j.match_score}%</span>` : '';
                    
                container.innerHTML += `
                    <div class="glass-card glow-cyan" style="padding-right: 80px;">
                        <span class="bookmark-badge ${isBookmarked ? 'active' : ''}" onclick="App.toggleJobBookmark(${j.id})">
                            <i class="${isBookmarked ? 'fas' : 'far'} fa-bookmark"></i>
                        </span>
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <div>
                                <h3 style="color:var(--text-primary)">${j.title}</h3>
                                <span style="font-size:13px; color:var(--text-secondary)">${j.company} &bull; ${j.location}</span>
                            </div>
                            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:6px;">
                                <span style="background:rgba(255,255,255,0.06); padding:4px 10px; border-radius:8px; font-size:12px;">${j.type}</span>
                                ${scoreBadge}
                            </div>
                        </div>
                        <p style="font-size:14px; color:var(--text-secondary); margin-bottom:16px;">${j.description}</p>
                        
                        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
                            ${j.skills_required.map(s => `<span style="font-size:11px; background:rgba(0,245,255,0.05); border:1px solid rgba(0,245,255,0.1); padding:4px 8px; border-radius:6px; color:var(--accent-secondary);">${s}</span>`).join('')}
                        </div>
                        
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:14px; font-weight:600; color:var(--success-color)">${j.salary}</span>
                            <a href="${j.link}" target="_blank" class="btn btn-secondary" style="padding: 8px 16px; font-size:13px;">Apply <i class="fas fa-external-link-alt"></i></a>
                        </div>
                    </div>
                `;
            });
            
        } catch (err) {
            console.error('Error loading jobs:', err);
        }
    },

    async toggleJobBookmark(jobId) {
        try {
            const res = await fetch('/api/jobs/bookmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeaders() },
                body: JSON.stringify({ job_id: jobId })
            });
            const data = await res.json();
            this.showNotification(data.message, 'success');
            this.loadJobsData();
            this.loadDashboardData();
        } catch (err) {
            this.showNotification(err.message, 'danger');
        }
    },

    // ----------------- SALARY PREDICTOR -----------------
    async runSalaryPrediction() {
        const role = document.getElementById('sal-role').value.trim();
        const stream = document.getElementById('sal-stream').value;
        const qualification = document.getElementById('sal-qual').value;
        const experience = parseFloat(document.getElementById('sal-experience').value) || 0.0;
        const skillsCount = (this.currentUser && Array.isArray(this.currentUser.current_skills)) ? this.currentUser.current_skills.length : 5;
        const locationType = document.getElementById('sal-location').value;
        
        if (!role) {
            this.showNotification('Please enter a target Job Role', 'warning');
            return;
        }
        
        try {
            const res = await fetch('/api/salary/predict', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    ...Auth.getAuthHeaders()
                },
                body: JSON.stringify({
                    role, stream, qualification, experience_years: experience, skills_count: skillsCount, location_type: locationType
                })
            });
            const data = await res.json();
            
            if (!res.ok) {
                this.showNotification(data.message || 'Salary prediction failed', 'danger');
                document.getElementById('sal-prediction-result-card').style.display = 'none';
                return;
            }
            
            document.getElementById('sal-prediction-result-card').style.display = 'block';
            document.getElementById('sal-predicted-salary').innerText = data.predicted_salary_range;
            document.getElementById('sal-matched-role').innerText = data.role;
            
            const factorsContainer = document.getElementById('sal-factors-breakdown');
            factorsContainer.innerHTML = '';
            
            data.breakdown.forEach(item => {
                factorsContainer.innerHTML += `
                    <div style="display:flex; justify-content:space-between; padding: 10px 0; border-bottom: 1px solid var(--card-border); font-size:14px;">
                        <span style="color:var(--text-secondary)">${item.factor}</span>
                        <span style="font-weight:600; color:var(--text-primary)">${item.value}</span>
                    </div>
                `;
            });
            
            document.getElementById('sal-prediction-result-card').scrollIntoView({ behavior: 'smooth' });
            
        } catch (err) {
            console.error('Error predicting salary:', err);
        }
    },

    // ----------------- RESUME BUILDER -----------------
    async loadResumeData() {
        try {
            // Load saved careers for target selector
            const res = await fetch('/api/careers/list');
            const careers = await res.json();
            const select = document.getElementById('res-target-career');
            select.innerHTML = '<option value="">Standard ATS Review (No Career Spec)</option>';
            careers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.title}</option>`;
            });
            
            // Load existing resume list
            const listRes = await fetch('/api/resume/list', { headers: Auth.getAuthHeaders() });
            const resumes = await listRes.json();
            
            const historyContainer = document.getElementById('res-history-list');
            historyContainer.innerHTML = '';
            
            if (resumes.length === 0) {
                historyContainer.innerHTML = '<p class="text-muted" style="font-size:13px;">No saved resumes found.</p>';
            } else {
                resumes.forEach(r => {
                    historyContainer.innerHTML += `
                        <div class="glass-card" style="padding: 12px 16px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <h4 style="font-size:14px;">${r.name} - ${r.template_name}</h4>
                                <span style="font-size:12px; color:var(--accent-secondary)">ATS: ${r.ats_score}%</span>
                            </div>
                            <div style="display:flex; gap:6px;">
                                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px;" onclick="App.editResume(${JSON.stringify(r).replace(/"/g, '&quot;')})">Edit</button>
                                <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px; color:var(--danger-color);" onclick="App.deleteResume(${r.id})">Delete</button>
                            </div>
                        </div>
                    `;
                });
            }
            
            // Trigger initial blank template preview
            this.updateResumePreview();
            
        } catch (err) {
            console.error('Error loading resume settings:', err);
        }
    },

    updateResumePreview() {
        const name = document.getElementById('res-name').value || 'APPLICANT NAME';
        const email = document.getElementById('res-email').value || 'email@example.com';
        const phone = document.getElementById('res-phone').value || '+91 99999 99999';
        const location = document.getElementById('res-location').value || 'City, India';
        const summary = document.getElementById('res-summary').value || 'A professional summary highlighting core strengths...';
        
        // Education List compilation
        const eduSchool = document.getElementById('res-edu-school').value;
        const eduDegree = document.getElementById('res-edu-degree').value;
        const eduYear = document.getElementById('res-edu-year').value;
        const eduCgpa = document.getElementById('res-edu-cgpa') ? document.getElementById('res-edu-cgpa').value : '';
        
        // Experience List compilation
        const expCompany = document.getElementById('res-exp-company').value;
        const expRole = document.getElementById('res-exp-role').value;
        const expDesc = document.getElementById('res-exp-desc').value;
        
        // Projects List
        const projTitle = document.getElementById('res-proj-title') ? document.getElementById('res-proj-title').value : '';
        const projDesc = document.getElementById('res-proj-desc') ? document.getElementById('res-proj-desc').value : '';

        // Certifications List
        const certNameField = document.getElementById('res-cert-name');
        const certifications = certNameField ? certNameField.value.split(',').map(s => s.trim()).filter(s => s) : [];

        // Skills List
        const skills = document.getElementById('res-skills').value.split(',').map(s => s.trim()).filter(s => s);
        
        // Update elements in iframe or mock preview panel
        document.getElementById('prev-name').innerText = name;
        document.getElementById('prev-contact').innerText = `${email} | ${phone} | ${location}`;
        document.getElementById('prev-summary').innerText = summary;
        
        const prevEdu = document.getElementById('prev-education');
        prevEdu.innerHTML = '';
        if (eduSchool || eduDegree) {
            const cgpaText = eduCgpa ? ` | CGPA/Grade: ${eduCgpa}` : '';
            prevEdu.innerHTML = `
                <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span>${eduDegree || 'Degree'}${cgpaText}</span>
                        <span>${eduYear || 'Year'}</span>
                    </div>
                    <div>${eduSchool || 'Institution Name'}</div>
                </div>
            `;
        }
        
        const prevExp = document.getElementById('prev-experience');
        prevExp.innerHTML = '';
        if (expCompany || expRole) {
            prevExp.innerHTML = `
                <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; font-weight:bold;">
                        <span>${expRole || 'Role'}</span>
                        <span>Present</span>
                    </div>
                    <div style="font-style:italic;">${expCompany || 'Company'}</div>
                    <p style="margin-top:4px; font-size:13px; line-height:1.4;">${expDesc || 'Responsibilities and highlights...'}</p>
                </div>
            `;
        }

        const prevProj = document.getElementById('prev-projects');
        if (prevProj) {
            prevProj.innerHTML = '';
            if (projTitle || projDesc) {
                prevProj.innerHTML = `
                    <div style="margin-bottom:8px;">
                        <div style="font-weight:bold;">${projTitle || 'Project Title'}</div>
                        <p style="margin-top:4px; font-size:12px; line-height:1.4; color:#333;">${projDesc || 'Project Description...'}</p>
                    </div>
                `;
            } else {
                prevProj.innerHTML = '<i>No projects added.</i>';
            }
        }

        const prevCert = document.getElementById('prev-certifications');
        if (prevCert) {
            prevCert.innerHTML = '';
            if (certifications.length > 0) {
                prevCert.innerHTML = `<div style="line-height:1.4;">${certifications.join(', ')}</div>`;
            } else {
                prevCert.innerHTML = '<i>No certifications added.</i>';
            }
        }
        
        const prevSkills = document.getElementById('prev-skills');
        prevSkills.innerHTML = '';
        if (skills.length > 0) {
            prevSkills.innerText = skills.join(', ');
        } else {
            prevSkills.innerText = 'Skill Keywords';
        }
    },

    async saveAndEvaluateResume() {
        const resumeData = {
            id: document.getElementById('res-id-holder').value || null,
            template_name: 'Modern Minimalist',
            name: document.getElementById('res-name').value.trim(),
            email: document.getElementById('res-email').value.trim(),
            phone: document.getElementById('res-phone').value.trim(),
            location: document.getElementById('res-location').value.trim(),
            summary: document.getElementById('res-summary').value.trim(),
            skills: document.getElementById('res-skills').value.split(',').map(s => s.trim()).filter(s => s),
            education: [
                {
                    school: document.getElementById('res-edu-school').value.trim(),
                    degree: document.getElementById('res-edu-degree').value.trim(),
                    year: document.getElementById('res-edu-year').value.trim(),
                    cgpa: document.getElementById('res-edu-cgpa') ? document.getElementById('res-edu-cgpa').value.trim() : ''
                }
            ],
            experience: [
                {
                    company: document.getElementById('res-exp-company').value.trim(),
                    role: document.getElementById('res-exp-role').value.trim(),
                    description: document.getElementById('res-exp-desc').value.trim()
                }
            ],
            projects: [
                {
                    title: document.getElementById('res-proj-title') ? document.getElementById('res-proj-title').value.trim() : '',
                    description: document.getElementById('res-proj-desc') ? document.getElementById('res-proj-desc').value.trim() : ''
                }
            ],
            certifications: document.getElementById('res-cert-name') ? document.getElementById('res-cert-name').value.split(',').map(c => c.trim()).filter(c => c) : [],
            target_career_id: document.getElementById('res-target-career').value
        };
        
        if (!resumeData.name || !resumeData.email) {
            this.showNotification('Please fill Name and Email details', 'warning');
            return;
        }
        
        try {
            const res = await fetch('/api/resume/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeaders() },
                body: JSON.stringify(resumeData)
            });
            const data = await res.json();
            
            this.showNotification(data.message, 'success');
            
            // Load ATS score
            const scoreCircle = document.getElementById('res-ats-score-gauge');
            scoreCircle.innerText = `${data.resume.ats_score}%`;
            
            // Remove colored classes
            scoreCircle.className = 'ats-gauge-circle';
            if (data.resume.ats_score >= 75) scoreCircle.classList.add('score-green');
            else if (data.resume.ats_score >= 50) scoreCircle.classList.add('score-orange');
            else scoreCircle.classList.add('score-red');
            
            // Suggestion list
            const sugList = document.getElementById('res-ats-suggestions');
            sugList.innerHTML = '';
            data.resume.feedback.suggestions.forEach(s => {
                sugList.innerHTML += `<li>${s}</li>`;
            });
            
            // Update Saved ID holder
            document.getElementById('res-id-holder').value = data.resume.id;
            
            this.loadResumeData();
            
        } catch (err) {
            console.error('Error saving resume:', err);
        }
    },

    editResume(resume) {
        document.getElementById('res-id-holder').value = resume.id;
        const templateSelect = document.getElementById('res-template-select');
        if (templateSelect) templateSelect.value = resume.template_name;
        document.getElementById('res-name').value = resume.name;
        document.getElementById('res-email').value = resume.email;
        document.getElementById('res-phone').value = resume.phone;
        document.getElementById('res-location').value = resume.location;
        document.getElementById('res-summary').value = resume.summary;
        document.getElementById('res-skills').value = resume.skills.join(', ');
        
        if (resume.education.length > 0) {
            document.getElementById('res-edu-school').value = resume.education[0].school || '';
            document.getElementById('res-edu-degree').value = resume.education[0].degree || '';
            document.getElementById('res-edu-year').value = resume.education[0].year || '';
            const eduCgpa = document.getElementById('res-edu-cgpa');
            if (eduCgpa) eduCgpa.value = resume.education[0].cgpa || '';
        }
        
        if (resume.experience.length > 0) {
            document.getElementById('res-exp-company').value = resume.experience[0].company || '';
            document.getElementById('res-exp-role').value = resume.experience[0].role || '';
            document.getElementById('res-exp-desc').value = resume.experience[0].description || '';
        }

        if (resume.projects && resume.projects.length > 0) {
            const projTitle = document.getElementById('res-proj-title');
            if (projTitle) projTitle.value = resume.projects[0].title || '';
            const projDesc = document.getElementById('res-proj-desc');
            if (projDesc) projDesc.value = resume.projects[0].description || '';
        } else {
            const projTitle = document.getElementById('res-proj-title');
            if (projTitle) projTitle.value = '';
            const projDesc = document.getElementById('res-proj-desc');
            if (projDesc) projDesc.value = '';
        }

        const certNameField = document.getElementById('res-cert-name');
        if (certNameField) {
            certNameField.value = resume.certifications ? resume.certifications.join(', ') : '';
        }
        
        this.updateResumePreview();
        this.showNotification('Resume details loaded to editor.', 'info');
    },

    async deleteResume(resumeId) {
        if (!confirm('Are you sure you want to delete this resume?')) return;
        try {
            const res = await fetch(`/api/resume/delete/${resumeId}`, {
                method: 'DELETE',
                headers: Auth.getAuthHeaders()
            });
            const data = await res.json();
            this.showNotification(data.message, 'success');
            this.loadResumeData();
        } catch (err) {
            console.error(err);
        }
    },

    downloadResumePDF() {
        // Triggers system printing using CSS print stylesheets mapped in style.css
        window.print();
    },

    // ----------------- SKILL GAP ANALYSIS -----------------
    async loadSkillsData() {
        try {
            const res = await fetch('/api/careers/list');
            const careers = await res.json();
            
            const select = document.getElementById('skill-target-career');
            select.innerHTML = '<option value="">Select Target Job Role...</option>';
            careers.forEach(c => {
                select.innerHTML += `<option value="${c.id}">${c.title}</option>`;
            });
        } catch (err) {
            console.error(err);
        }
    },

    async runSkillGapAnalysis() {
        const careerId = document.getElementById('skill-target-career').value;
        if (!careerId) {
            this.showNotification('Please select a target career path to analyze', 'warning');
            return;
        }
        
        try {
            const res = await fetch('/api/skills/gap-analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeaders() },
                body: JSON.stringify({ career_id: careerId })
            });
            const data = await res.json();
            
            document.getElementById('skills-result-panel').style.display = 'block';
            
            // Skill match percentage fill
            const fill = document.getElementById('skill-match-fill');
            fill.style.width = `${data.match_percentage}%`;
            document.getElementById('skill-match-pct-text').innerText = `${data.match_percentage}%`;
            
            // Match and Missing list
            const matchedContainer = document.getElementById('skill-matched-list');
            matchedContainer.innerHTML = '';
            data.matching_skills.forEach(s => {
                matchedContainer.innerHTML += `<span style="background:rgba(0, 230, 118, 0.1); color:var(--success-color); border:1px solid rgba(0, 230, 118, 0.2); padding: 6px 12px; border-radius: 12px; font-size:13px; font-weight:600;">${s}</span>`;
            });
            if (data.matching_skills.length === 0) matchedContainer.innerHTML = '<span class="text-muted">None. Update your profile skills first!</span>';
            
            const missingContainer = document.getElementById('skill-missing-list');
            missingContainer.innerHTML = '';
            data.missing_skills.forEach(s => {
                missingContainer.innerHTML += `<span style="background:rgba(255, 51, 102, 0.1); color:var(--danger-color); border:1px solid rgba(255, 51, 102, 0.2); padding: 6px 12px; border-radius: 12px; font-size:13px; font-weight:600;">${s}</span>`;
            });
            if (data.missing_skills.length === 0) missingContainer.innerHTML = '<span class="text-muted">None! You possess all required technical skills.</span>';
            
            // Courses
            const coursesBox = document.getElementById('skill-courses-container');
            coursesBox.innerHTML = '';
            if (data.recommended_courses.length === 0) {
                coursesBox.innerHTML = '<p class="text-muted">No specific courses needed.</p>';
            } else {
                data.recommended_courses.forEach(c => {
                    coursesBox.innerHTML += `
                        <div class="glass-card" style="padding:16px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <h4 style="font-size:14px; color:var(--text-primary);">${c.title}</h4>
                                <span style="font-size:12px; color:var(--text-secondary);">${c.platform} &bull; ${c.provider}</span>
                            </div>
                            <a href="${c.link}" target="_blank" class="btn btn-secondary" style="padding:6px 12px; font-size:12px;">Enroll <i class="fas fa-external-link-alt"></i></a>
                        </div>
                    `;
                });
            }
            
            // Detailed Roadmap phases
            const roadmapBox = document.getElementById('skill-roadmap-timeline');
            roadmapBox.innerHTML = '';
            data.learning_roadmap.forEach((phase, idx) => {
                roadmapBox.innerHTML += `
                    <div class="roadmap-node ${idx === 0 ? 'active' : ''}">
                        <div class="roadmap-dot"></div>
                        <div class="roadmap-content">
                            <h3>${phase.title}</h3>
                            <p style="font-size:13px; color:var(--text-secondary); margin-top:4px;">${phase.description}</p>
                            <div style="font-size:13px; font-weight:600; color:var(--accent-secondary); margin: 8px 0;">Duration: ${phase.estimated_duration}</div>
                            <ul style="padding-left: 20px; font-size:13px; color:var(--text-primary); line-height:1.5;">
                                ${phase.suggested_actions.map(action => `<li>${action}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('skills-result-panel').scrollIntoView({ behavior: 'smooth' });
            
        } catch (err) {
            console.error('Error running skill gap analysis:', err);
        }
    },



    // ----------------- ADMIN DASHBOARD -----------------
    async loadAdminData() {
        try {
            const res = await fetch('/api/admin/metrics', { headers: Auth.getAuthHeaders() });
            if (!res.ok) {
                this.showNotification('Admin access forbidden. Redirecting to login.', 'danger');
                Auth.clearToken();
                this.currentUser = null;
                document.getElementById('nav-user-box').style.display = 'none';
                document.getElementById('nav-admin').style.display = 'none';
                this.updateSidebarNavigation();
                this.switchView('login');
                return;
            }
            
            const metrics = await res.json();
            document.getElementById('admin-total-users').innerText = metrics.users_count;
            document.getElementById('admin-total-resumes').innerText = metrics.resumes_count;
            document.getElementById('admin-total-jobs').innerText = metrics.jobs_count;

            
            // Load admin jobs list
            const jobsRes = await fetch('/api/jobs/list');
            const jobs = await jobsRes.json();
            
            const jobsTable = document.getElementById('admin-jobs-table-body');
            jobsTable.innerHTML = '';
            
            jobs.forEach(j => {
                jobsTable.innerHTML += `
                    <tr>
                        <td style="padding:10px; border-bottom:1px solid var(--card-border);">${j.title}</td>
                        <td style="padding:10px; border-bottom:1px solid var(--card-border);">${j.company}</td>
                        <td style="padding:10px; border-bottom:1px solid var(--card-border);">${j.location}</td>
                        <td style="padding:10px; border-bottom:1px solid var(--card-border);">${j.type}</td>
                        <td style="padding:10px; border-bottom:1px solid var(--card-border);">
                            <button class="btn btn-secondary" style="padding:4px 8px; font-size:11px; color:var(--danger-color);" onclick="App.deleteJobAdmin(${j.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
            
            // Load admin students details
            const studentsRes = await fetch('/api/admin/students', { headers: Auth.getAuthHeaders() });
            if (studentsRes.ok) {
                const students = await studentsRes.json();
                this.adminStudents = students;
                const studentsTable = document.getElementById('admin-students-table-body');
                studentsTable.innerHTML = '';
                
                if (students.length === 0) {
                    studentsTable.innerHTML = '<tr><td colspan="7" style="padding:16px; text-align:center;" class="text-muted">No students registered yet.</td></tr>';
                } else {
                    students.forEach(s => {
                        const skillsBadges = s.skills.map(sk => `<span style="font-size:10px; background:rgba(138,43,226,0.06); padding:2px 6px; border-radius:4px; margin-right:4px; display:inline-block;">${sk}</span>`).join('');
                        const interestsBadges = s.interests.map(i => `<span style="font-size:10px; background:rgba(0,245,255,0.06); padding:2px 6px; border-radius:4px; margin-right:4px; display:inline-block;">${i}</span>`).join('');
                        
                        studentsTable.innerHTML += `
                            <tr>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border); font-weight:600;">${s.full_name || s.username}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border); color:var(--text-secondary);">${s.email}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border); color:var(--accent-secondary);">${s.stream}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border);">${s.qualification}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border); max-width: 250px;">${skillsBadges || 'None'}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border); max-width: 200px;">${interestsBadges || 'None'}</td>
                                <td style="padding:12px; border-bottom:1px solid var(--card-border);">
                                    <button class="btn btn-secondary" style="padding: 6px 12px; font-size:11px; display:inline-flex; align-items:center; gap:4px;" onclick="App.viewStudentDetails(${s.id})">
                                        <i class="fa-solid fa-eye"></i> Details
                                    </button>
                                </td>
                            </tr>
                        `;
                    });
                }
            }
            
        } catch (err) {
            console.error(err);
        }
    },

    viewStudentDetails(studentId) {
        if (!this.adminStudents) return;
        const student = this.adminStudents.find(s => s.id === studentId);
        if (!student) return;

        // Set name and email
        document.getElementById('modal-student-name').innerText = student.full_name || student.username;
        document.getElementById('modal-student-email').innerText = student.email;

        // Tab 1: Profile & Details
        document.getElementById('modal-age').innerText = student.age || 'Not Set';
        document.getElementById('modal-stream').innerText = student.stream || 'Not Set';
        document.getElementById('modal-qualification').innerText = student.qualification || 'Not Set';
        document.getElementById('modal-academic').innerText = student.academic_performance || 'Not Set';
        document.getElementById('modal-experience').innerText = student.experience_years !== null ? `${student.experience_years} Years` : '0 Years';
        document.getElementById('modal-goal').innerText = student.target_goal || 'Not Set';
        document.getElementById('modal-bio').innerText = student.bio || 'No bio written yet.';

        // Skills Badges
        const skillsContainer = document.getElementById('modal-skills-list');
        skillsContainer.innerHTML = '';
        if (student.skills.length === 0) {
            skillsContainer.innerHTML = '<span class="text-muted" style="font-size:13px;">No skills added yet.</span>';
        } else {
            student.skills.forEach(sk => {
                skillsContainer.innerHTML += `<span class="badge" style="background:rgba(138,43,226,0.1); border:1px solid rgba(138,43,226,0.2); padding:6px 12px; border-radius:12px; font-size:12px; color:var(--text-primary);">${sk}</span>`;
            });
        }

        // Interests Badges
        const interestsContainer = document.getElementById('modal-interests-list');
        interestsContainer.innerHTML = '';
        if (student.interests.length === 0) {
            interestsContainer.innerHTML = '<span class="text-muted" style="font-size:13px;">No interests added yet.</span>';
        } else {
            student.interests.forEach(i => {
                interestsContainer.innerHTML += `<span class="badge" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.2); padding:6px 12px; border-radius:12px; font-size:12px; color:var(--text-primary);">${i}</span>`;
            });
        }



        // Tab 3: Activity & Resumes
        const resumesContainer = document.getElementById('modal-resumes-list');
        resumesContainer.innerHTML = '';
        if (student.resumes.length === 0) {
            resumesContainer.innerHTML = '<p class="text-muted" style="font-size:13px; padding: 10px 0;">No resumes generated yet.</p>';
        } else {
            student.resumes.forEach(r => {
                let scoreClass = 'score-red';
                if (r.ats_score >= 70) scoreClass = 'score-green';
                else if (r.ats_score >= 40) scoreClass = 'score-orange';

                resumesContainer.innerHTML += `
                    <div class="glass-card" style="margin-bottom:10px; padding:12px; background:rgba(255,255,255,0.02); display:flex; justify-content:space-between; align-items:center; border-radius:12px;">
                        <div>
                            <h5 style="color:var(--text-primary); margin-bottom:2px;">${r.name}</h5>
                            <span style="font-size:11px; color:var(--text-muted);">${r.template_name}</span>
                        </div>
                        <div style="text-align:right;">
                            <div class="ats-gauge-circle ${scoreClass}" style="width:40px; height:40px; font-size:12px; border-width:3px; margin:0 auto 2px auto;">${r.ats_score}%</div>
                            <span style="font-size:10px; color:var(--text-secondary)">ATS Score</span>
                        </div>
                    </div>
                `;
            });
        }

        // Bookmarked Careers
        const savedCareersContainer = document.getElementById('modal-saved-careers');
        savedCareersContainer.innerHTML = '';
        if (student.saved_careers.length === 0) {
            savedCareersContainer.innerHTML = '<span class="text-muted">No career paths bookmarked.</span>';
        } else {
            student.saved_careers.forEach(c => {
                savedCareersContainer.innerHTML += `<li>${c}</li>`;
            });
        }

        // Bookmarked Jobs
        const savedJobsContainer = document.getElementById('modal-saved-jobs');
        savedJobsContainer.innerHTML = '';
        if (student.saved_jobs.length === 0) {
            savedJobsContainer.innerHTML = '<span class="text-muted">No jobs bookmarked.</span>';
        } else {
            student.saved_jobs.forEach(j => {
                savedJobsContainer.innerHTML += `<li>${j}</li>`;
            });
        }

        // Reset to Profile Tab
        this.switchModalTab('profile');

        // Show Modal
        document.getElementById('admin-student-modal').style.display = 'flex';
    },

    closeStudentModal() {
        document.getElementById('admin-student-modal').style.display = 'none';
    },

    showCourseDetails(course) {
        if (!course) return;
        
        document.getElementById('modal-course-title').innerText = course.title || 'N/A';
        document.getElementById('modal-course-platform-provider').innerHTML = `${course.platform || 'N/A'} &bull; ${course.provider || 'N/A'}`;
        document.getElementById('modal-course-difficulty').innerText = course.difficulty || 'Beginner';
        document.getElementById('modal-course-duration').innerText = course.duration || 'N/A';
        document.getElementById('modal-course-rating').innerText = `${course.rating || 4.5} / 5.0`;
        document.getElementById('modal-course-category').innerText = course.skill_category || 'N/A';
        
        const enrollBtn = document.getElementById('modal-course-enroll-btn');
        if (enrollBtn) {
            enrollBtn.href = course.link || '#';
        }
        
        document.getElementById('course-details-modal').style.display = 'flex';
    },
    
    closeCourseModal() {
        document.getElementById('course-details-modal').style.display = 'none';
    },

    switchModalTab(tabId) {
        // Toggle tab button states
        document.querySelectorAll('.modal-tab-btn').forEach(btn => {
            if (btn.id === `btn-tab-${tabId}`) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Toggle tab content display
        document.querySelectorAll('.modal-tab-content').forEach(content => {
            if (content.id === `modal-tab-content-${tabId}`) {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        });
    },

    async deleteJobAdmin(jobId) {
        if (!confirm('Are you sure you want to delete this job ad?')) return;
        try {
            const res = await fetch(`/api/admin/jobs?id=${jobId}`, {
                method: 'DELETE',
                headers: Auth.getAuthHeaders()
            });
            if (res.ok) {
                this.showNotification('Job deleted successfully', 'success');
                this.loadAdminData();
            }
        } catch (err) {
            console.error(err);
        }
    },

    async createJobAdmin() {
        const jobData = {
            title: document.getElementById('adm-job-title').value.trim(),
            company: document.getElementById('adm-job-company').value.trim(),
            description: document.getElementById('adm-job-desc').value.trim(),
            type: document.getElementById('adm-job-type').value,
            location: document.getElementById('adm-job-location').value.trim(),
            skills_required: document.getElementById('adm-job-skills').value.split(',').map(s => s.trim()).filter(s => s),
            salary: document.getElementById('adm-job-salary').value.trim(),
            experience_required: parseFloat(document.getElementById('adm-job-experience').value) || 0.0,
            link: document.getElementById('adm-job-link').value.trim()
        };
        
        if (!jobData.title || !jobData.company) {
            this.showNotification('Title and Company fields are required', 'warning');
            return;
        }
        
        try {
            const res = await fetch('/api/admin/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...Auth.getAuthHeaders() },
                body: JSON.stringify(jobData)
            });
            
            if (res.ok) {
                this.showNotification('Job created successfully!', 'success');
                // Clear fields
                document.getElementById('adm-job-title').value = '';
                document.getElementById('adm-job-company').value = '';
                document.getElementById('adm-job-desc').value = '';
                document.getElementById('adm-job-location').value = '';
                document.getElementById('adm-job-skills').value = '';
                document.getElementById('adm-job-salary').value = '';
                document.getElementById('adm-job-experience').value = '';
                document.getElementById('adm-job-link').value = '';
                
                this.loadAdminData();
            }
        } catch (err) {
            console.error(err);
        }
    },

    // ----------------- EVENT INITIALIZER -----------------
    setupEventListeners() {
        // Dashboard
        const saveProfile = document.getElementById('btn-save-profile');
        if (saveProfile) saveProfile.addEventListener('click', () => this.saveProfileData());
        
        // Careers Search
        const careerSearch = document.getElementById('career-search');
        if (careerSearch) {
            careerSearch.addEventListener('input', () => this.loadCareersData());
        }
        const careerFilter = document.getElementById('career-stream-filter');
        if (careerFilter) {
            careerFilter.addEventListener('change', () => this.loadCareersData());
        }
        
        // Compare Button
        const compareBtn = document.getElementById('btn-execute-compare');
        if (compareBtn) {
            compareBtn.addEventListener('click', () => this.runComparison());
        }
        
        // Jobs Search
        const jobSearch = document.getElementById('job-search-input');
        if (jobSearch) jobSearch.addEventListener('input', () => this.loadJobsData());
        
        const jobType = document.getElementById('job-type-filter');
        if (jobType) jobType.addEventListener('change', () => this.loadJobsData());
        
        const jobLoc = document.getElementById('job-location-input');
        if (jobLoc) jobLoc.addEventListener('input', () => this.loadJobsData());
        
        const jobToggle = document.getElementById('job-ai-recommend-toggle');
        if (jobToggle) jobToggle.addEventListener('change', () => this.loadJobsData());
        
        // Salary Predictor
        const predictSalaryBtn = document.getElementById('btn-execute-salary');
        if (predictSalaryBtn) {
            predictSalaryBtn.addEventListener('click', () => this.runSalaryPrediction());
        }
        
        // Resume editor updates
        const resumeFields = ['res-name', 'res-email', 'res-phone', 'res-location', 'res-summary', 
                            'res-edu-school', 'res-edu-degree', 'res-edu-year', 'res-edu-cgpa',
                            'res-exp-company', 'res-exp-role', 'res-exp-desc',
                            'res-proj-title', 'res-proj-desc', 'res-cert-name', 'res-skills'];
        resumeFields.forEach(id => {
            const field = document.getElementById(id);
            if (field) field.addEventListener('input', () => this.updateResumePreview());
        });
        
        const saveResumeBtn = document.getElementById('btn-save-resume');
        if (saveResumeBtn) {
            saveResumeBtn.addEventListener('click', () => this.saveAndEvaluateResume());
        }
        
        const downloadResumeBtn = document.getElementById('btn-download-resume');
        if (downloadResumeBtn) {
            downloadResumeBtn.addEventListener('click', () => this.downloadResumePDF());
        }
        
        // Skill Gap Analyzer
        const skillAnalyzeBtn = document.getElementById('btn-execute-skills');
        if (skillAnalyzeBtn) {
            skillAnalyzeBtn.addEventListener('click', () => this.runSkillGapAnalysis());
        }
        

        

        
        // Admin
        const createJobBtn = document.getElementById('btn-admin-add-job');
        if (createJobBtn) createJobBtn.addEventListener('click', () => this.createJobAdmin());

        // Close student modal when clicking on the backdrop overlay
        const modalOverlay = document.getElementById('admin-student-modal');
        if (modalOverlay) {
            modalOverlay.addEventListener('click', (e) => {
                if (e.target === modalOverlay) {
                    this.closeStudentModal();
                }
            });
        }

        // Close course modal when clicking on the backdrop overlay
        const courseModalOverlay = document.getElementById('course-details-modal');
        if (courseModalOverlay) {
            courseModalOverlay.addEventListener('click', (e) => {
                if (e.target === courseModalOverlay) {
                    this.closeCourseModal();
                }
            });
        }
    },
    
    updateSidebarNavigation() {
        const role = Auth.getUserRole();
        const isLoggedIn = Auth.isLoggedIn();
        
        // Find elements
        const studentNavs = document.querySelectorAll('nav a[data-view="careers"], nav a[data-view="skills"], nav a[data-view="resume"], nav a[data-view="jobs"], nav a[data-view="salary"]');
        const dashNav = document.querySelector('nav a[data-view="dashboard"]');
        
        if (isLoggedIn) {
            const loginLink = document.getElementById('nav-login-link');
            if (loginLink) {
                loginLink.style.display = 'none';
            }
            if (dashNav) {
                dashNav.style.display = 'flex';
            }
            if (role === 'admin') {
                // Hide student navs
                studentNavs.forEach(nav => nav.style.display = 'none');
                // Update Dashboard text to Admin Dashboard
                if (dashNav) {
                    dashNav.querySelector('span').innerText = 'Admin Dashboard';
                }
            } else {
                // Show student navs
                studentNavs.forEach(nav => nav.style.display = 'flex');
                if (dashNav) {
                    dashNav.querySelector('span').innerText = 'Dashboard';
                }
            }
        } else {
            // Not logged in
            const loginLink = document.getElementById('nav-login-link');
            if (loginLink) {
                loginLink.style.display = 'flex';
            }
            studentNavs.forEach(nav => nav.style.display = 'none');
            if (dashNav) {
                dashNav.style.display = 'none';
            }
        }

        // Update user avatar in sidebar
        const navAvatar = document.getElementById('nav-avatar');
        if (navAvatar) {
            if (isLoggedIn) {
                const username = Auth.getUsername() || 'U';
                navAvatar.innerText = username.charAt(0).toUpperCase();
            } else {
                navAvatar.innerText = 'U';
            }
        }
    }
};

// Expose functions globally for dynamic onclick handlers in templates
window.App = App;
