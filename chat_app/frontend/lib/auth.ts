interface LoginData {
  email?: string;
  username?: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  grade: string;
}

interface User {
  username: string;
  email: string;
  created_at: string;
  grade: string;
  full_name?: string;
  profile_picture?: string;
  auth_provider?: string;
  streak_data?: {
    current_streak: number;
    longest_streak: number;
    streak_history: string[];
    last_active_date?: string;
  };
}

const API_URL = 'http://localhost:5000'; // Flask default port

export const authService = {
  async login(data: LoginData) {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    const result = await response.json();
    
    if (!response.ok) {
      throw new Error(result.message || 'Failed to login');
    }
    
    if (result.access_token) {
      localStorage.setItem('token', result.access_token);
      console.log(result.access_token);
    }
    
    return result;
  },

  async register(data: RegisterData) {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    const result = await response.json();
    
    if (!response.ok) {
      if (result.errors) {
        throw new Error(result.errors.join(', '));
      }
      throw new Error(result.message || 'Failed to register');
    }
    
    if (result.access_token) {
      localStorage.setItem('token', result.access_token);
    }
    
    return result;
  },

  async logout() {
    const token = this.getToken();
    if (!token) return;

    try {
      const response = await fetch(`${API_URL}/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to logout');
      }
    } finally {
      localStorage.removeItem('token');
    }
  },

  async getUser(): Promise<User | null> {
    const token = this.getToken();
    if (!token) return null;

    try {
      const response = await fetch(`${API_URL}/user`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }

      const result = await response.json();
      return result.user;
    } catch (error) {
      console.error('Error fetching user data:', error);
      return null;
    }
  },

  getToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  handleTokenExpiration() {
    // Clear token and expiration
    localStorage.removeItem('token');
    localStorage.removeItem('tokenExpiration');
    
    // Redirect to login page using window.location
    // This ensures a clean state after logout
    window.location.href = '/login';
  },

  // This function is called when the user is active
  updateActivity: async (): Promise<void> => {
    const token = localStorage.getItem('token');
    if (!token) return;
    
    try {
      await fetch('http://localhost:5000/api/user/activity', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Failed to update activity:', error);
    }
  },

  async initiateGoogleLogin() {
    try {
      const response = await fetch(`${API_URL}/auth/google`);
      const data = await response.json();
      
      if (data.auth_url) {
        // Redirect to Google's authentication page
        window.location.href = data.auth_url;
      } else {
        throw new Error('Failed to initiate Google login');
      }
    } catch (error) {
      console.error('Error initiating Google login:', error);
      throw error;
    }
  },
  
  async handleGoogleCallback(code: string) {
    try {
      if (!code || code.length < 10) {
        console.error('Invalid authorization code received:', code);
        throw new Error('Invalid authorization code');
      }

      console.log('Starting Google callback handling with code length:', code.length);
      
      // Mark that we're processing this code
      const processKey = `processed_${code.substring(0, 10)}`;
      
      // Check if this code was already processed to prevent duplicates
      if (typeof window !== 'undefined' && sessionStorage.getItem(processKey)) {
        console.warn('This authorization code has already been processed');
        return null; // Return null to indicate processing was skipped
      }
      
      // Mark this code as being processed
      if (typeof window !== 'undefined') {
        sessionStorage.setItem(processKey, 'true');
      }
      
      const response = await fetch(`${API_URL}/auth/google/callback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code })
      });
      
      // Get the response as text first for debugging
      const responseText = await response.text();
      console.log(`Response status: ${response.status}, length: ${responseText.length}`);
      
      // Parse the response if possible
      let result;
      try {
        result = JSON.parse(responseText);
      } catch (parseError) {
        console.error('Error parsing response:', parseError);
        throw new Error(`Failed to parse server response: ${responseText.substring(0, 100)}`);
      }
      
      if (!response.ok) {
        console.error('Google callback error response:', result);
        
        // Handle specific error cases
        if (result.message && result.message.includes('already used')) {
          // Redirect to login page with appropriate error
          console.log('Auth code already used, redirecting to login page');
          if (typeof window !== 'undefined') {
            window.location.href = '/login?error=code_already_used';
            return null; // Return null to prevent further processing
          }
        }
        
        throw new Error(result.message || `Authentication failed: ${response.status}`);
      }
      
      console.log('Google callback successful, token received');
      
      if (result.access_token) {
        localStorage.setItem('token', result.access_token);
        
        // Also store user data if available
        if (result.user) {
          localStorage.setItem('user', JSON.stringify(result.user));
        }
        
        return result;
      } else {
        console.error('No access token in response:', result);
        throw new Error('No access token received');
      }
    } catch (error) {
      console.error('Error handling Google callback:', error);
      throw error;
    }
  },
};