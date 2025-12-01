import React, { useState, useEffect } from 'react';
import api from '../services/api';

interface Quiz {
  id: number;
  title: string;
}

const QuizList: React.FC = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const response = await api.get('/quizzes/');
        console.log('res:', response);
        setQuizzes(response.data);
      } catch (error) {
        setError('Failed to load quizzes. Please check your authentication.');
      }
    };

    fetchQuizzes();
  }, []);

  return (
    <div>
      <h2>Available Quizzes</h2>
      {error && <p>{error}</p>}
      <ul>
        {quizzes.map((quiz) => (
          <li key={quiz.id}>
            <a href={`/quizzes/${quiz.id}`}>{quiz.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default QuizList;
