import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Quiz {
  id: number;
  title: string;
  description?: string;
  total_points?: number;
  question_count?: number;
  difficulty_level?: string;
  time_limit_minutes?: number | null;
  category?: { id: number; name: string; description?: string } | null;
  tags?: { id: number; name: string }[];
}

const QuizList: React.FC = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState<Quiz[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [categories, setCategories] = useState<{id: number, name: string}[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        setLoading(true);
        const response = await api.get('/quizzes/');
        console.log('res:', response);
        setQuizzes(response.data);
        setFilteredQuizzes(response.data);

        // Extract unique categories
        const uniqueCategories = response.data
          .filter((q: Quiz) => q.category)
          .map((q: Quiz) => q.category!)
          .filter((cat: { id: number; name: string; description?: string }, index: number, self: { id: number; name: string; description?: string }[]) =>
            self.findIndex(c => c.id === cat.id) === index
          );
        setCategories(uniqueCategories);

        setError(null);
      } catch (error) {
        setError('Failed to load quizzes. Please check your authentication.');
      } finally {
        setLoading(false);
      }
    };

    fetchQuizzes();
  }, []);

  useEffect(() => {
    let filtered = quizzes;

    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter(q => q.difficulty_level === selectedDifficulty);
    }

    if (selectedCategory) {
      filtered = filtered.filter(q => q.category?.id === selectedCategory);
    }

    setFilteredQuizzes(filtered);
  }, [selectedDifficulty, selectedCategory, quizzes]);

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
        marginBottom: 'var(--space-xl)',
        flexWrap: 'wrap',
        gap: 'var(--space-md)'
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
            {filteredQuizzes.length} Quiz{filteredQuizzes.length !== 1 ? 'zes' : ''} Found
          </span>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: 'var(--space-lg)' }}>
        <h3 style={{ marginBottom: 'var(--space-md)', fontSize: '1.1rem' }}>🔍 Filter Quizzes</h3>
        <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap' }}>
          {/* Difficulty Filter */}
          <div style={{ flex: 1, minWidth: '200px' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Difficulty Level
            </label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-main)',
                fontSize: '1rem',
                cursor: 'pointer'
              }}
            >
              <option value="all">All Levels</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {/* Category Filter */}
          {categories.length > 0 && (
            <div style={{ flex: 1, minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                Category
              </label>
              <select
                value={selectedCategory || ''}
                onChange={(e) => setSelectedCategory(e.target.value ? parseInt(e.target.value) : null)}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--text-main)',
                  fontSize: '1rem',
                  cursor: 'pointer'
                }}
              >
                <option value="">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
          )}

          {/* Clear Filters */}
          {(selectedDifficulty !== 'all' || selectedCategory) && (
            <div style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  setSelectedDifficulty('all');
                  setSelectedCategory(null);
                }}
              >
                Clear Filters
              </button>
            </div>
          )}
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

      {filteredQuizzes.length === 0 && !error ? (
        <div className="card" style={{
          textAlign: 'center',
          padding: 'var(--space-xl)'
        }}>
          <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>📚</div>
          <h3 style={{ marginBottom: 'var(--space-sm)' }}>No Quizzes Found</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            Try adjusting your filters or check back later for new quizzes!
          </p>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
          gap: 'var(--space-lg)'
        }}>
          {filteredQuizzes.map((quiz, index) => (
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

              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', marginBottom: 'var(--space-sm)' }}>
                <h3 style={{
                  margin: 0,
                  fontSize: '1.25rem',
                  color: 'var(--text-main)',
                  flex: 1
                }}>
                  {quiz.title}
                </h3>
                {quiz.difficulty_level && (
                  <span style={{
                    padding: '0.25rem 0.5rem',
                    background: quiz.difficulty_level === 'easy' ? 'rgba(16, 185, 129, 0.2)' :
                               quiz.difficulty_level === 'hard' ? 'rgba(239, 68, 68, 0.2)' :
                               'rgba(251, 191, 36, 0.2)',
                    color: quiz.difficulty_level === 'easy' ? '#10b981' :
                           quiz.difficulty_level === 'hard' ? '#ef4444' : '#fbbf24',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    textTransform: 'capitalize'
                  }}>
                    {quiz.difficulty_level}
                  </span>
                )}
              </div>

              {quiz.category && (
                <div style={{ marginBottom: 'var(--space-sm)' }}>
                  <span style={{
                    display: 'inline-block',
                    padding: '0.25rem 0.75rem',
                    background: 'rgba(99, 102, 241, 0.1)',
                    borderRadius: 'var(--radius-full)',
                    fontSize: '0.8rem',
                    color: 'var(--primary-light)'
                  }}>
                    📚 {quiz.category.name}
                  </span>
                </div>
              )}

              <p style={{
                color: 'var(--text-muted)',
                marginBottom: 'var(--space-md)',
                lineHeight: 1.6,
                minHeight: '3em'
              }}>
                {quiz.description || 'Test your knowledge with this quiz'}
              </p>

              {quiz.tags && quiz.tags.length > 0 && (
                <div style={{
                  display: 'flex',
                  gap: '0.5rem',
                  flexWrap: 'wrap',
                  marginBottom: 'var(--space-md)'
                }}>
                  {quiz.tags.slice(0, 3).map((tag) => (
                    <span key={tag.id} style={{
                      padding: '0.25rem 0.5rem',
                      background: 'rgba(139, 92, 246, 0.1)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '0.7rem',
                      color: 'var(--accent)'
                    }}>
                      #{tag.name}
                    </span>
                  ))}
                </div>
              )}

              <div style={{
                display: 'flex',
                gap: 'var(--space-md)',
                paddingTop: 'var(--space-md)',
                borderTop: '1px solid rgba(255, 255, 255, 0.05)',
                flexWrap: 'wrap'
              }}>
                {quiz.question_count && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    color: 'var(--text-muted)',
                    fontSize: '0.9rem'
                  }}>
                    <span style={{ color: 'var(--secondary)' }}>❓</span>
                    <span>{quiz.question_count} questions</span>
                  </div>
                )}
                {quiz.time_limit_minutes && (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    color: 'var(--text-muted)',
                    fontSize: '0.9rem'
                  }}>
                    <span style={{ color: 'var(--accent)' }}>⏱️</span>
                    <span>{quiz.time_limit_minutes} min</span>
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
