import { useState, useEffect } from 'react';
import api from '../services/api';

interface Answer {
  id: number;
  text: string;
}

interface Question {
  id: number;
  text: string;
  question_type: string;
  points: number;
  answers: Answer[];
}

interface Quiz {
  id: number;
  title: string;
  description: string;
  questions: Question[];
  total_points: number;
}

interface UseQuizResult {
  quiz: Quiz | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useQuiz = (quizId: string | undefined): UseQuizResult => {
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuiz = async (): Promise<void> => {
    if (!quizId) {
      setError('Quiz ID is required');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await api.get(`/quizzes/${quizId}/`);
      setQuiz(response.data);
    } catch (err: any) {
      console.error('Error fetching quiz:', err);
      const errorMessage =
        err.response?.data?.error?.message ||
        err.response?.data?.detail ||
        'Failed to load quiz. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuiz();
  }, [quizId]);

  return {
    quiz,
    loading,
    error,
    refetch: fetchQuiz,
  };
};
