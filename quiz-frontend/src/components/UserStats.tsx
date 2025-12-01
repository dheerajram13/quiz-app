import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface UserStatsData {
    total_quizzes: number;
    average_score: number;
    highest_score: number;
}

const UserStats: React.FC = () => {
    const [stats, setStats] = useState<UserStatsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchStats = async () => {
            try {
                setLoading(true);
                const response = await api.get('/quizzes/user_stats/');
                setStats(response.data as UserStatsData);
                setError(null);
            } catch (error) {
                console.error("Error fetching user stats:", error);
                setError("Failed to load statistics. Please try again later.");
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    const getPerformanceLevel = (avgScore: number) => {
        if (avgScore >= 80) return { label: 'Excellent', color: 'var(--success)', emoji: '🌟' };
        if (avgScore >= 60) return { label: 'Good', color: 'var(--primary-light)', emoji: '👍' };
        if (avgScore >= 40) return { label: 'Fair', color: 'var(--warning)', emoji: '📈' };
        return { label: 'Keep Learning', color: 'var(--text-muted)', emoji: '📚' };
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
                <div className="spinner" style={{ width: '50px', height: '50px', margin: '0 auto 1rem' }} />
                <p style={{ color: 'var(--text-muted)' }}>Loading your statistics...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card animate-fade-in" style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
                <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>⚠️</div>
                <h2 style={{ marginBottom: 'var(--space-md)' }}>Error</h2>
                <p style={{ color: 'var(--error)', marginBottom: 'var(--space-lg)' }}>{error}</p>
                <button className="btn btn-primary" onClick={() => window.location.reload()}>
                    Try Again
                </button>
            </div>
        );
    }

    if (!stats) {
        return null;
    }

    const performance = getPerformanceLevel(stats.average_score);

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div style={{ marginBottom: 'var(--space-xl)' }}>
                <h1 style={{ marginBottom: '0.5rem' }}>Your Statistics</h1>
                <p style={{ color: 'var(--text-muted)', margin: 0 }}>
                    Track your progress and achievements
                </p>
            </div>

            {/* No stats yet */}
            {stats.total_quizzes === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
                    <div style={{ fontSize: '5rem', marginBottom: 'var(--space-md)' }}>🎯</div>
                    <h2 style={{ marginBottom: 'var(--space-md)' }}>No Quizzes Taken Yet</h2>
                    <p style={{ color: 'var(--text-muted)', marginBottom: 'var(--space-lg)', maxWidth: '400px', margin: '0 auto var(--space-lg)' }}>
                        Start your learning journey by taking your first quiz!
                    </p>
                    <button className="btn btn-primary" onClick={() => navigate('/quizzes')}>
                        Browse Quizzes
                    </button>
                </div>
            ) : (
                <>
                    {/* Performance Overview */}
                    <div className="card" style={{
                        marginBottom: 'var(--space-lg)',
                        background: 'var(--gradient-primary)',
                        textAlign: 'center',
                        position: 'relative',
                        overflow: 'hidden'
                    }}>
                        <div style={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            fontSize: '15rem',
                            opacity: 0.1
                        }}>
                            {performance.emoji}
                        </div>
                        <div style={{ position: 'relative', zIndex: 1 }}>
                            <div style={{ fontSize: '4rem', marginBottom: 'var(--space-sm)' }}>
                                {performance.emoji}
                            </div>
                            <h2 style={{ marginBottom: 'var(--space-sm)' }}>Performance: {performance.label}</h2>
                            <p style={{ fontSize: '1.1rem', opacity: 0.9, margin: 0 }}>
                                You've completed {stats.total_quizzes} quiz{stats.total_quizzes !== 1 ? 'zes' : ''}
                            </p>
                        </div>
                    </div>

                    {/* Stats Grid */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                        gap: 'var(--space-lg)',
                        marginBottom: 'var(--space-lg)'
                    }}>
                        {/* Total Quizzes */}
                        <div className="card" style={{
                            textAlign: 'center',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                right: 0,
                                height: '4px',
                                background: 'var(--gradient-primary)'
                            }} />
                            <div style={{
                                width: '80px',
                                height: '80px',
                                margin: '0 auto var(--space-md)',
                                background: 'rgba(99, 102, 241, 0.2)',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '2.5rem'
                            }}>
                                📊
                            </div>
                            <div style={{
                                fontSize: '3rem',
                                fontWeight: 'bold',
                                background: 'var(--gradient-primary)',
                                WebkitBackgroundClip: 'text',
                                WebkitTextFillColor: 'transparent',
                                marginBottom: 'var(--space-sm)'
                            }}>
                                {stats.total_quizzes}
                            </div>
                            <h3 style={{ fontSize: '1.1rem', color: 'var(--text-muted)', margin: 0 }}>
                                Quiz{stats.total_quizzes !== 1 ? 'zes' : ''} Completed
                            </h3>
                        </div>

                        {/* Average Score */}
                        <div className="card" style={{
                            textAlign: 'center',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                right: 0,
                                height: '4px',
                                background: `linear-gradient(135deg, ${performance.color} 0%, var(--accent) 100%)`
                            }} />
                            <div style={{
                                width: '80px',
                                height: '80px',
                                margin: '0 auto var(--space-md)',
                                background: 'rgba(236, 72, 153, 0.2)',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '2.5rem'
                            }}>
                                📈
                            </div>
                            <div style={{
                                fontSize: '3rem',
                                fontWeight: 'bold',
                                color: performance.color,
                                marginBottom: 'var(--space-sm)'
                            }}>
                                {stats.average_score.toFixed(1)}%
                            </div>
                            <h3 style={{ fontSize: '1.1rem', color: 'var(--text-muted)', margin: 0 }}>
                                Average Score
                            </h3>
                            {/* Progress Bar */}
                            <div style={{
                                marginTop: 'var(--space-md)',
                                height: '8px',
                                background: 'rgba(255, 255, 255, 0.1)',
                                borderRadius: 'var(--radius-full)',
                                overflow: 'hidden'
                            }}>
                                <div style={{
                                    width: `${stats.average_score}%`,
                                    height: '100%',
                                    background: performance.color,
                                    borderRadius: 'var(--radius-full)',
                                    transition: 'width 1s ease-out'
                                }} />
                            </div>
                        </div>

                        {/* Highest Score */}
                        <div className="card" style={{
                            textAlign: 'center',
                            position: 'relative',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                right: 0,
                                height: '4px',
                                background: 'linear-gradient(135deg, #f59e0b 0%, #eab308 100%)'
                            }} />
                            <div style={{
                                width: '80px',
                                height: '80px',
                                margin: '0 auto var(--space-md)',
                                background: 'rgba(245, 158, 11, 0.2)',
                                borderRadius: '50%',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '2.5rem'
                            }}>
                                🏆
                            </div>
                            <div style={{
                                fontSize: '3rem',
                                fontWeight: 'bold',
                                color: 'var(--warning)',
                                marginBottom: 'var(--space-sm)'
                            }}>
                                {stats.highest_score.toFixed(1)}%
                            </div>
                            <h3 style={{ fontSize: '1.1rem', color: 'var(--text-muted)', margin: 0 }}>
                                Best Score
                            </h3>
                            {/* Progress Bar */}
                            <div style={{
                                marginTop: 'var(--space-md)',
                                height: '8px',
                                background: 'rgba(255, 255, 255, 0.1)',
                                borderRadius: 'var(--radius-full)',
                                overflow: 'hidden'
                            }}>
                                <div style={{
                                    width: `${stats.highest_score}%`,
                                    height: '100%',
                                    background: 'var(--warning)',
                                    borderRadius: 'var(--radius-full)',
                                    transition: 'width 1s ease-out'
                                }} />
                            </div>
                        </div>
                    </div>

                    {/* Achievements Section */}
                    <div className="card">
                        <h2 style={{ marginBottom: 'var(--space-lg)' }}>🎖️ Achievements</h2>
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                            gap: 'var(--space-md)'
                        }}>
                            {/* First Quiz */}
                            <div style={{
                                padding: 'var(--space-md)',
                                background: stats.total_quizzes >= 1 ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                                border: `1px solid ${stats.total_quizzes >= 1 ? 'rgba(99, 102, 241, 0.3)' : 'rgba(255, 255, 255, 0.05)'}`,
                                borderRadius: 'var(--radius-md)',
                                textAlign: 'center',
                                opacity: stats.total_quizzes >= 1 ? 1 : 0.5
                            }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: 'var(--space-sm)' }}>🎯</div>
                                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.25rem' }}>First Steps</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Complete 1 quiz</div>
                            </div>

                            {/* Five Quizzes */}
                            <div style={{
                                padding: 'var(--space-md)',
                                background: stats.total_quizzes >= 5 ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                                border: `1px solid ${stats.total_quizzes >= 5 ? 'rgba(99, 102, 241, 0.3)' : 'rgba(255, 255, 255, 0.05)'}`,
                                borderRadius: 'var(--radius-md)',
                                textAlign: 'center',
                                opacity: stats.total_quizzes >= 5 ? 1 : 0.5
                            }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: 'var(--space-sm)' }}>🔥</div>
                                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.25rem' }}>On Fire</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Complete 5 quizzes</div>
                            </div>

                            {/* Perfect Score */}
                            <div style={{
                                padding: 'var(--space-md)',
                                background: stats.highest_score === 100 ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                                border: `1px solid ${stats.highest_score === 100 ? 'rgba(99, 102, 241, 0.3)' : 'rgba(255, 255, 255, 0.05)'}`,
                                borderRadius: 'var(--radius-md)',
                                textAlign: 'center',
                                opacity: stats.highest_score === 100 ? 1 : 0.5
                            }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: 'var(--space-sm)' }}>💯</div>
                                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.25rem' }}>Perfect!</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Score 100%</div>
                            </div>

                            {/* High Performer */}
                            <div style={{
                                padding: 'var(--space-md)',
                                background: stats.average_score >= 80 ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                                border: `1px solid ${stats.average_score >= 80 ? 'rgba(99, 102, 241, 0.3)' : 'rgba(255, 255, 255, 0.05)'}`,
                                borderRadius: 'var(--radius-md)',
                                textAlign: 'center',
                                opacity: stats.average_score >= 80 ? 1 : 0.5
                            }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: 'var(--space-sm)' }}>⭐</div>
                                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.25rem' }}>Superstar</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Avg. score 80%+</div>
                            </div>
                        </div>
                    </div>

                    {/* Action Button */}
                    <div style={{ textAlign: 'center', marginTop: 'var(--space-xl)' }}>
                        <button
                            className="btn btn-primary"
                            onClick={() => navigate('/quizzes')}
                            style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}
                        >
                            Take Another Quiz →
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default UserStats;
