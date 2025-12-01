import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const { isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const isActive = (path: string) => location.pathname === path;

    return (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            {isAuthenticated && (
                <nav style={{
                    background: 'rgba(15, 23, 42, 0.8)',
                    backdropFilter: 'blur(10px)',
                    borderBottom: '1px solid rgba(255,255,255,0.05)',
                    position: 'sticky',
                    top: 0,
                    zIndex: 100
                }}>
                    <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '70px' }}>
                        <Link to="/quizzes" style={{ fontSize: '1.5rem', fontWeight: 'bold', background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                            QuizApp
                        </Link>
                        <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                            <Link
                                to="/quizzes"
                                style={{
                                    color: isActive('/quizzes') ? 'var(--primary-light)' : 'var(--text-muted)',
                                    fontWeight: isActive('/quizzes') ? 600 : 400
                                }}
                            >
                                Quizzes
                            </Link>
                            <Link
                                to="/user-stats"
                                style={{
                                    color: isActive('/user-stats') ? 'var(--primary-light)' : 'var(--text-muted)',
                                    fontWeight: isActive('/user-stats') ? 600 : 400
                                }}
                            >
                                My Stats
                            </Link>
                            <button
                                onClick={handleLogout}
                                className="btn btn-secondary"
                                style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </nav>
            )}

            <main style={{ flex: 1, padding: '40px 0' }}>
                <div className="container">
                    {children}
                </div>
            </main>

            <footer style={{
                textAlign: 'center',
                padding: '20px',
                color: 'var(--text-muted)',
                fontSize: '0.9rem',
                borderTop: '1px solid rgba(255,255,255,0.05)'
            }}>
                <p>© {new Date().getFullYear()} QuizApp. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default Layout;
