import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Quiz {
  id: number;
  title: string;
  description?: string;
  total_points?: number;
  questions_count?: number;
}

const QuizList: React.FC = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        setLoading(true);
        const response = await api.get('/quizzes/');
        console.log('res:', response);
        setQuizzes(response.data);
        setError(null);
      } catch (error) {
        setError('Failed to load quizzes. Please check your authentication.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuizzes();
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <div className="spinner" style={{ width: '50px', height: '50px', margin: '0 auto 1rem' }} />
        <p style={{ color: 'var(--text-muted)' }}>Loading quizzes...</p>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 'var(--space-xl)'
      }}>
        <div>
          <h1 style={{ marginBottom: '0.5rem' }}>Available Quizzes</h1>
          <p style={{ color: 'var(--text-muted)', margin: 0 }}>
            Choose a quiz to test your knowledge
          </p>
        </div>
        <div style={{
          padding: '0.75rem 1.5rem',
          background: 'rgba(99, 102, 241, 0.1)',
          borderRadius: 'var(--radius-full)',
          border: '1px solid rgba(99, 102, 241, 0.3)'
        }}>
          <span style={{ fontSize: '0.9rem', color: 'var(--primary-light)', fontWeight: 600 }}>
            {quizzes.length} Quiz{quizzes.length !== 1 ? 'zes' : ''} Available
          </span>
        </div>
      </div>

      {error && (
        <div style={{
          padding: 'var(--space-lg)',
          background: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid var(--error)',
          borderRadius: 'var(--radius-lg)',
          marginBottom: 'var(--space-lg)',
          color: 'var(--error)',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <span style={{ fontSize: '1.5rem' }}>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {quizzes.length === 0 && !error ? (
        <div className="card" style={{
          textAlign: 'center',
          padding: 'var(--space-xl)'
        }}>
          <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>📚</div>
          <h3 style={{ marginBottom: 'var(--space-sm)' }}>No Quizzes Available</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            Check back later for new quizzes!
          </p>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
          gap: 'var(--space-lg)'
        }}>
          {quizzes.map((quiz, index) => (
            <div
              key={quiz.id}
              className="card"
              style={{
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                position: 'relative',
                overflow: 'hidden',
                animation: `fadeIn 0.5s ease-out ${index * 0.1}s forwards`,
                opacity: 0
              }}
              onClick={() => navigate(`/quizzes/${quiz.id}`)}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-glow)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'var(--shadow-lg)';
              }}
            >
              {/* Gradient accent bar */}
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'var(--gradient-primary)'
              }} />

              {/* Quiz icon/badge */}
              <div style={{
                width: '60px',
                height: '60px',
                background: 'var(--gradient-primary)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2rem',
                marginBottom: 'var(--space-md)',
                boxShadow: 'var(--shadow-md)'
              }}>
                📝
              </div>

              <h3 style={{
                marginBottom: 'var(--space-sm)',
                fontSize: '1.25rem',
                color: 'var(--text-main)'
              }}>
                {quiz.title}
              </h3>

              <p style={{
                color: 'var(--text-muted)',
                marginBottom: 'var(--space-md)',
                lineHeight: 1.6,
                minHeight: '3em'
              }}>
                {quiz.description || 'Test your knowledge with this quiz'}
              </p>

              <div style={{
                display: 'flex',
                gap: 'var(--space-md)',
                paddingTop: 'var(--space-md)',
                borderTop: '1px solid rgba(255, 255, 255, 0.05)'
              }}>
                {quiz.total_points && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    color: 'var(--text-muted)',
                    fontSize: '0.9rem'
                  }}>
                    <span style={{ color: 'var(--primary-light)' }}>⭐</span>
                    <span>{quiz.total_points} pts</span>
                  </div>
                )}
                {quiz.questions_count && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    color: 'var(--text-muted)',
                    fontSize: '0.9rem'
                  }}>
                    <span style={{ color: 'var(--secondary)' }}>❓</span>
                    <span>{quiz.questions_count} questions</span>
                  </div>
                )}
              </div>

              <button
                className="btn btn-primary"
                style={{
                  width: '100%',
                  marginTop: 'var(--space-md)'
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/quizzes/${quiz.id}`);
                }}
              >
                Start Quiz →
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QuizList;
