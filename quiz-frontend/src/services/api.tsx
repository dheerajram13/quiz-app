import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { storage } from '../constants/storage';
import { AuthTokens } from '../types';

// Use environment variable for API URL with fallback for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/';

const api: AxiosInstance = axios.create({
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
      const response = await axios.post<AuthTokens>(`${API_URL}token/refresh/`, { refresh });
      const { access } = response.data;
      storage.setAccessToken(access);
      if (api.defaults.headers.common) {
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      }
      return access;
    } catch (error: unknown) {
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
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = storage.getAccessToken();
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => Promise.reject(error)
);

// Extend InternalAxiosRequestConfig to include _retry property
interface RetryableAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

// Handle 401 errors by trying to refresh the token
api.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => response,
  async (error: AxiosError): Promise<AxiosResponse | AxiosError> => {
    const originalRequest = error.config as RetryableAxiosRequestConfig;
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest) {
      originalRequest._retry = true;
      const newAccessToken = await refreshToken();
      if (newAccessToken && originalRequest.headers) {
        // Update authorization header and retry the request
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
