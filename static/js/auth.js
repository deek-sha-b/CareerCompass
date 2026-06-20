// Auth Manager for Career Guidance System

const Auth = {
    getToken() {
        return localStorage.getItem('career_jwt_token');
    },

    setToken(token) {
        localStorage.setItem('career_jwt_token', token);
    },

    clearToken() {
        localStorage.removeItem('career_jwt_token');
        localStorage.removeItem('career_username');
        localStorage.removeItem('career_role');
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    getUserRole() {
        return localStorage.getItem('career_role') || 'student';
    },

    getUsername() {
        return localStorage.getItem('career_username') || 'User';
    },

    getAuthHeaders() {
        const token = this.getToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    },

    async login(username, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }

            this.setToken(data.token);
            localStorage.setItem('career_username', data.username);
            localStorage.setItem('career_role', data.role);

            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    async register(username, email, password, role) {
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password, role })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Registration failed');
            }

            return data;
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    },

    async getProfile() {
        if (!this.isLoggedIn()) return null;
        try {
            const response = await fetch('/api/auth/profile', {
                headers: {
                    ...this.getAuthHeaders()
                }
            });
            const data = await response.json();
            if (!response.ok) {
                if (response.status === 401 || response.status === 404) {
                    this.clearToken();
                    window.location.reload();
                }
                throw new Error(data.message || 'Failed to fetch profile');
            }
            return data;
        } catch (error) {
            console.error('Profile fetch error:', error);
            return null;
        }
    },

    async updateProfile(profileData) {
        if (!this.isLoggedIn()) return null;
        try {
            const response = await fetch('/api/auth/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: JSON.stringify(profileData)
            });
            const data = await response.json();
            if (!response.ok) {
                if (response.status === 401 || response.status === 404) {
                    this.clearToken();
                    window.location.reload();
                }
                const err = new Error(data.message || 'Failed to update profile');
                err.response = data;
                throw err;
            }
            return data;
        } catch (error) {
            console.error('Profile update error:', error);
            throw error;
        }
    }
};

window.Auth = Auth;
