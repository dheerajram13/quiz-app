import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setLocalError(null);
      await login(username, password);
      console.log('Login successful');
      navigate('/quizzes');
    } catch (error: any) {
      console.error('Login failed:', error);
      setLocalError(error.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {localError && <div style={{ color: 'red', marginBottom: '10px' }}>{localError}</div>}
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        disabled={isLoading}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
        disabled={isLoading}
      />
      <button onClick={handleLogin} disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </div>
  );
};

export default Login;
