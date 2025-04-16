// Base URL for API
const API_BASE_URL = 'http://localhost:8000';

async function apiRequest(endpoint, method = 'GET', data = null, token = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const options = {
        method,
        headers,
        credentials: 'include'
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        // Handle non-JSON responses (like 204 No Content)
        if (response.status === 204) {
            return { success: true };
        }
        
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.detail || 'Something went wrong');
        }
        
        return responseData;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

function saveToken(token) {
    localStorage.setItem('token', token);
}

function getToken() {
    return localStorage.getItem('token');
}

function removeToken() {
    localStorage.removeItem('token');
}

function saveUserData(userData) {
    localStorage.setItem('user', JSON.stringify(userData));
}

function getUserData() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData): null;
}

function removeUserData() {
    localStorage.removeItem('user');
}

function isLoggedIn() {
    return !!getToken();
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

function showSuccess(elementId, message) {
    const successElement = document.getElementById(elementId);
    if (successElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function getRoleBadgeClass(role) {
    switch (role) {
        case 'admin':
            return 'admin-badge';
        case 'developer':
            return 'developer-badge';
        case 'viewer':
            return 'viewer-badge';
        default:
            return '';
    }
}