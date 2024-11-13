import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Answer {
  id: number;
  text: string;
}

interface Question {
  id: number;
  text: string;
  question_type: string;
  answers: Answer[];
}

const Quiz: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, number[]>>({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchQuiz = async () => {
      const token = localStorage.getItem('token');
      const response = await api.get(`/quizzes/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('Quiz:', response.data);
      setQuestions(response.data.questions);
    };
    fetchQuiz();
  }, [id]);

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
    try {
      const token = localStorage.getItem('token');
      const payload = {
        quiz_id: id,  // Add the quiz_id to the payload
        answers
      };
      const response = await api.post(`/quizzes/${id}/submit/`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert(`Score: ${response.data.score}`);
      navigate('/user-stats');
    } catch (error) {
      console.error(error); // Log the error for debugging
      alert('Submission failed');
    }
  };
  

  return (
    <div>
      <h2>Quiz</h2>
      {questions.map((q) => (
        <div key={q.id}>
          <p>{q.text}</p>
          {q.answers.map((a) => (
            <label key={a.id}>
              <input
                type={q.question_type === 'single' ? 'radio' : 'checkbox'}
                name={`question-${q.id}`}
                value={a.id}
                onChange={(e) => handleAnswerChange(q.id, a.id, e.target.checked)}
              />
              {a.text}
            </label>
          ))}
        </div>
      ))}
      <button onClick={handleSubmit}>Submit Answers</button>
    </div>
  );
};

export default Quiz;
