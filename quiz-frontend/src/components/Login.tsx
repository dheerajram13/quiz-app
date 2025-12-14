import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (): Promise<void> => {
    try {
      setLocalError(null);
      await login(username, password);
      console.log('Login successful');
      navigate('/quizzes');
    } catch (error: unknown) {
      console.error('Login failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      setLocalError(errorMessage);
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '80vh'
    }}>
      <div className="card animate-fade-in" style={{
        maxWidth: '440px',
        width: '100%',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Decorative gradient overlay */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '4px',
          background: 'var(--gradient-primary)'
        }} />

        <div style={{ textAlign: 'center', marginBottom: 'var(--space-xl)' }}>
          <div style={{
            width: '80px',
            height: '80px',
            margin: '0 auto 20px',
            background: 'var(--gradient-primary)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2.5rem',
            boxShadow: 'var(--shadow-glow)'
          }}>
            🧠
          </div>
          <h1 style={{ marginBottom: '0.5rem', fontSize: '2rem' }}>Welcome Back</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0 }}>
            Sign in to continue your learning journey
          </p>
        </div>

        {localError && (
          <div style={{
            padding: 'var(--space-md)',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid var(--error)',
            borderRadius: 'var(--radius-md)',
            marginBottom: 'var(--space-lg)',
            color: 'var(--error)',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span style={{ fontSize: '1.2rem' }}>⚠️</span>
            <span>{localError}</span>
          </div>
        )}

        <form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
          <div className="input-group">
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: 600,
              color: 'var(--text-main)'
            }}>
              Username
            </label>
            <input
              type="text"
              placeholder="Enter your username"
              className="input-field"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
              autoComplete="username"
            />
          </div>

          <div className="input-group">
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: 600,
              color: 'var(--text-main)'
            }}>
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              disabled={isLoading}
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading || !username || !password}
            style={{
              width: '100%',
              marginTop: 'var(--space-md)',
              fontSize: '1.1rem',
              padding: '1rem'
            }}
          >
            {isLoading ? (
              <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                <span className="spinner" />
                Logging in...
              </span>
            ) : 'Sign In'}
          </button>
        </form>

        <div style={{
          marginTop: 'var(--space-lg)',
          padding: 'var(--space-md)',
          background: 'rgba(99, 102, 241, 0.05)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(99, 102, 241, 0.2)'
        }}>
          <p style={{
            margin: 0,
            fontSize: '0.9rem',
            color: 'var(--text-muted)',
            textAlign: 'center'
          }}>
            Demo credentials: <strong style={{ color: 'var(--primary-light)' }}>admin / admin</strong>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
