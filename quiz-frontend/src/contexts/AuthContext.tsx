import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../services/api';
import { storage } from '../constants/storage';
import { User, AuthTokens } from '../types';
import { getErrorMessage } from '../types/errors';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(storage.isAuthenticated());
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async (): Promise<void> => {
      const accessToken = storage.getAccessToken();
      if (accessToken) {
        try {
          // Optionally, fetch user details from a /me endpoint
          // For now, just set authenticated state
          setIsAuthenticated(true);
        } catch (err: unknown) {
          console.error('Auth check failed:', err);
          storage.clearTokens();
          setIsAuthenticated(false);
        }
      } else {
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string): Promise<void> => {
    try {
      setError(null);
      setIsLoading(true);
      const response = await api.post<AuthTokens>('/token/', { username, password });

      const { access, refresh } = response.data;
      storage.setTokens(access, refresh);

      // Optionally set user data if available
      // setUser(response.data.user);

      setIsAuthenticated(true);
    } catch (err: unknown) {
      const errorMessage = getErrorMessage(err, 'Login failed. Please check your credentials.');
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = (): void => {
    storage.clearTokens();
    setUser(null);
    setIsAuthenticated(false);
    window.location.href = '/login';
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
