import axios from 'axios';
import { storage } from '../constants/storage';

// Use environment variable for API URL with fallback for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to refresh the access token
const refreshToken = async (): Promise<string | null> => {
  const refresh = storage.getRefreshToken();
  if (refresh) {
    try {
      const response = await axios.post(`${API_URL}token/refresh/`, { refresh });
      const { access } = response.data;
      storage.setAccessToken(access);
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      return access;
    } catch (error) {
      console.error('Error refreshing token:', error);
      storage.clearTokens();
      // Redirect to login page
      window.location.href = '/login';
      return null;
    }
  }
  return null;
};

// Add the access token to request headers if available
api.interceptors.request.use(
  (config) => {
    const token = storage.getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 errors by trying to refresh the token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newAccessToken = await refreshToken();
      if (newAccessToken) {
        // Update authorization header and retry the request
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
