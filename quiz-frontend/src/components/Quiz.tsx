import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuiz } from '../hooks/useQuiz';
import { useQuizSubmit } from '../hooks/useQuizSubmit';

const Quiz: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [answers, setAnswers] = useState<Record<number, number[]>>({});
  const [showResultModal, setShowResultModal] = useState(false);
  const [result, setResult] = useState<any>(null);
  const navigate = useNavigate();

  const { quiz, loading, error: fetchError } = useQuiz(id);
  const { submitQuiz, submitting, error: submitError } = useQuizSubmit();

  const error = fetchError || submitError;

  const handleAnswerChange = (questionId: number, answerId: number, isSelected: boolean, questionType: string) => {
    setAnswers((prev) => {
      if (questionType === 'single') {
        return { ...prev, [questionId]: isSelected ? [answerId] : [] };
      } else {
        const selectedAnswers = prev[questionId] || [];
        if (isSelected) {
          return { ...prev, [questionId]: [...selectedAnswers, answerId] };
        } else {
          return { ...prev, [questionId]: selectedAnswers.filter((id) => id !== answerId) };
        }
      }
    });
  };

  const handleSubmit = async () => {
    if (!id) return;

    try {
      const submitResult = await submitQuiz(id, answers);
      setResult(submitResult);
      setShowResultModal(true);
    } catch (err) {
      console.error('Submission failed');
    }
  };

  const getAnsweredCount = () => {
    return Object.keys(answers).filter(key => {
      const answerArray = answers[parseInt(key)];
      return answerArray && answerArray.length > 0;
    }).length;
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <div className="spinner" style={{ width: '50px', height: '50px', margin: '0 auto 1rem' }} />
        <p style={{ color: 'var(--text-muted)' }}>Loading quiz...</p>
      </div>
    );
  }

  if (error && !quiz) {
    return (
      <div className="card animate-fade-in" style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
        <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>⚠️</div>
        <h2 style={{ marginBottom: 'var(--space-md)' }}>Error</h2>
        <p style={{ color: 'var(--error)', marginBottom: 'var(--space-lg)' }}>{error}</p>
        <button className="btn btn-primary" onClick={() => navigate('/quizzes')}>
          Back to Quizzes
        </button>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="card animate-fade-in" style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
        <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>🔍</div>
        <h2 style={{ marginBottom: 'var(--space-md)' }}>Quiz Not Found</h2>
        <button className="btn btn-primary" onClick={() => navigate('/quizzes')}>
          Back to Quizzes
        </button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Quiz Header */}
      <div className="card" style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 'var(--space-md)' }}>
          <div style={{ flex: 1 }}>
            <h1 style={{ marginBottom: 'var(--space-sm)' }}>{quiz.title}</h1>
            <p style={{ color: 'var(--text-muted)', marginBottom: 'var(--space-md)' }}>
              {quiz.description}
            </p>
          </div>
          <div style={{
            padding: '0.75rem 1.5rem',
            background: 'var(--gradient-primary)',
            borderRadius: 'var(--radius-full)',
            whiteSpace: 'nowrap',
            marginLeft: 'var(--space-md)'
          }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{quiz.total_points}</div>
            <div style={{ fontSize: '0.8rem', opacity: 0.9 }}>Total Points</div>
          </div>
        </div>

        <div style={{
          display: 'flex',
          gap: 'var(--space-md)',
          padding: 'var(--space-md)',
          background: 'rgba(99, 102, 241, 0.05)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(99, 102, 241, 0.2)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.2rem' }}>📝</span>
            <span style={{ color: 'var(--text-muted)' }}>
              {quiz.questions.length} Questions
            </span>
          </div>
          <div style={{ borderLeft: '1px solid rgba(255, 255, 255, 0.1)' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.2rem' }}>✓</span>
            <span style={{ color: 'var(--text-muted)' }}>
              {getAnsweredCount()} / {quiz.questions.length} Answered
            </span>
          </div>
        </div>
      </div>

      {error && (
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
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Questions */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
        {quiz.questions.map((q, index) => (
          <div key={q.id} className="card" style={{ position: 'relative' }}>
            {/* Question number badge */}
            <div style={{
              position: 'absolute',
              top: '-12px',
              left: 'var(--space-lg)',
              background: 'var(--gradient-primary)',
              padding: '0.5rem 1rem',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.9rem',
              fontWeight: 'bold',
              boxShadow: 'var(--shadow-md)'
            }}>
              Question {index + 1}
            </div>

            <div style={{ marginTop: 'var(--space-sm)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 'var(--space-md)' }}>
                <p style={{
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  color: 'var(--text-main)',
                  margin: 0,
                  flex: 1
                }}>
                  {q.text}
                </p>
                <div style={{
                  padding: '0.25rem 0.75rem',
                  background: 'rgba(139, 92, 246, 0.2)',
                  borderRadius: 'var(--radius-full)',
                  fontSize: '0.85rem',
                  color: 'var(--accent)',
                  fontWeight: 600,
                  marginLeft: 'var(--space-md)',
                  whiteSpace: 'nowrap'
                }}>
                  {q.points} {q.points === 1 ? 'point' : 'points'}
                </div>
              </div>

              {q.question_type === 'multiple' && (
                <div style={{
                  padding: '0.5rem 0.75rem',
                  background: 'rgba(16, 185, 129, 0.1)',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem',
                  color: 'var(--success)',
                  marginBottom: 'var(--space-md)',
                  display: 'inline-block'
                }}>
                  Multiple answers allowed
                </div>
              )}

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                {q.answers.map((a) => {
                  const isSelected = (answers[q.id] || []).includes(a.id);
                  return (
                    <label
                      key={a.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: 'var(--space-md)',
                        background: isSelected ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                        border: `2px solid ${isSelected ? 'var(--primary)' : 'rgba(255, 255, 255, 0.05)'}`,
                        borderRadius: 'var(--radius-md)',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => {
                        if (!isSelected) {
                          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                          e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.5)';
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!isSelected) {
                          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.02)';
                          e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.05)';
                        }
                      }}
                    >
                      <input
                        type={q.question_type === 'single' ? 'radio' : 'checkbox'}
                        name={`question-${q.id}`}
                        value={a.id}
                        checked={isSelected}
                        onChange={(e) => handleAnswerChange(q.id, a.id, e.target.checked, q.question_type)}
                        disabled={submitting}
                        style={{ marginRight: 'var(--space-md)', cursor: 'pointer' }}
                      />
                      <span style={{ color: 'var(--text-main)', fontSize: '1rem' }}>{a.text}</span>
                    </label>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className="card" style={{
        marginTop: 'var(--space-lg)',
        display: 'flex',
        gap: 'var(--space-md)',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/quizzes')}
          disabled={submitting}
        >
          ← Back to Quizzes
        </button>
        <button
          className="btn btn-primary"
          onClick={handleSubmit}
          disabled={submitting || getAnsweredCount() === 0}
          style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}
        >
          {submitting ? (
            <span style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span className="spinner" />
              Submitting...
            </span>
          ) : (
            `Submit ${getAnsweredCount() > 0 ? `(${getAnsweredCount()} answers)` : ''}`
          )}
        </button>
      </div>

      {/* Result Modal */}
      {showResultModal && result && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          backdropFilter: 'blur(4px)'
        }} onClick={() => {
          setShowResultModal(false);
          navigate('/user-stats');
        }}>
          <div className="card" style={{
            maxWidth: '500px',
            width: '90%',
            textAlign: 'center',
            animation: 'fadeIn 0.3s ease-out'
          }} onClick={(e) => e.stopPropagation()}>
            <div style={{
              fontSize: '5rem',
              marginBottom: 'var(--space-md)'
            }}>
              {result.score >= 80 ? '🎉' : result.score >= 60 ? '👍' : '📚'}
            </div>
            <h2 style={{ marginBottom: 'var(--space-md)' }}>Quiz Completed!</h2>

            <div style={{
              padding: 'var(--space-lg)',
              background: 'var(--gradient-primary)',
              borderRadius: 'var(--radius-lg)',
              marginBottom: 'var(--space-lg)'
            }}>
              <div style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                {result.score}%
              </div>
              <div style={{ fontSize: '1.1rem', opacity: 0.9 }}>Your Score</div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: 'var(--space-md)',
              marginBottom: 'var(--space-lg)'
            }}>
              <div style={{
                padding: 'var(--space-md)',
                background: 'rgba(99, 102, 241, 0.1)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid rgba(99, 102, 241, 0.3)'
              }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-light)' }}>
                  {result.earned_points}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Points Earned</div>
              </div>
              <div style={{
                padding: 'var(--space-md)',
                background: 'rgba(99, 102, 241, 0.1)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid rgba(99, 102, 241, 0.3)'
              }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-light)' }}>
                  {result.total_points}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Total Points</div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
              <button
                className="btn btn-secondary"
                onClick={() => {
                  setShowResultModal(false);
                  navigate('/quizzes');
                }}
                style={{ flex: 1 }}
              >
                Back to Quizzes
              </button>
              <button
                className="btn btn-primary"
                onClick={() => {
                  setShowResultModal(false);
                  navigate('/user-stats');
                }}
                style={{ flex: 1 }}
              >
                View Stats
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Quiz;
