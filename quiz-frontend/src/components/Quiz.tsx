import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuiz } from '../hooks/useQuiz';
import { useQuizSubmit } from '../hooks/useQuizSubmit';

const Quiz: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [answers, setAnswers] = useState<Record<number, number[]>>({});
  const navigate = useNavigate();

  const { quiz, loading, error: fetchError } = useQuiz(id);
  const { submitQuiz, submitting, error: submitError } = useQuizSubmit();

  const error = fetchError || submitError;

  const handleAnswerChange = (questionId: number, answerId: number, isSelected: boolean) => {
    setAnswers((prev) => {
      const selectedAnswers = prev[questionId] || [];
      if (isSelected) {
        return { ...prev, [questionId]: [...selectedAnswers, answerId] };
      } else {
        return { ...prev, [questionId]: selectedAnswers.filter((id) => id !== answerId) };
      }
    });
  };

  const handleSubmit = async () => {
    if (!id) return;

    try {
      const result = await submitQuiz(id, answers);
      alert(
        `Score: ${result.score}%\nTotal Points: ${result.total_points}\nEarned Points: ${result.earned_points}`
      );
      navigate('/user-stats');
    } catch (err) {
      // Error is already handled in the hook
      console.error('Submission failed');
    }
  };

  if (loading) {
    return (
      <div>
        <h2>Loading Quiz...</h2>
        <p>Please wait while we load the quiz.</p>
      </div>
    );
  }

  if (error && !quiz) {
    return (
      <div>
        <h2>Error</h2>
        <p style={{ color: 'red' }}>{error}</p>
        <button onClick={() => navigate('/quizzes')}>Back to Quizzes</button>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div>
        <h2>Quiz Not Found</h2>
        <button onClick={() => navigate('/quizzes')}>Back to Quizzes</button>
      </div>
    );
  }

  return (
    <div>
      <h2>{quiz.title}</h2>
      <p>{quiz.description}</p>
      <p><em>Total Points: {quiz.total_points}</em></p>
      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      {quiz.questions.map((q) => (
        <div key={q.id} style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}>
          <p><strong>{q.text}</strong> ({q.points} point{q.points !== 1 ? 's' : ''})</p>
          {q.answers.map((a) => (
            <label key={a.id} style={{ display: 'block', marginLeft: '20px', marginTop: '5px' }}>
              <input
                type={q.question_type === 'single' ? 'radio' : 'checkbox'}
                name={`question-${q.id}`}
                value={a.id}
                onChange={(e) => handleAnswerChange(q.id, a.id, e.target.checked)}
                disabled={submitting}
              />
              {' '}{a.text}
            </label>
          ))}
        </div>
      ))}
      <button onClick={handleSubmit} disabled={submitting} style={{ padding: '10px 20px', marginRight: '10px' }}>
        {submitting ? 'Submitting...' : 'Submit Answers'}
      </button>
      <button onClick={() => navigate('/quizzes')} disabled={submitting} style={{ padding: '10px 20px' }}>
        Back to Quizzes
      </button>
    </div>
  );
};

export default Quiz;
