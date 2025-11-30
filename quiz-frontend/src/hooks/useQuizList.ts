import { useState, useEffect } from 'react';
import api from '../services/api';

interface QuizListItem {
  id: number;
  title: string;
  description: string;
  question_count: number;
  created_at: string;
}

interface UseQuizListResult {
  quizzes: QuizListItem[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useQuizList = (): UseQuizListResult => {
  const [quizzes, setQuizzes] = useState<QuizListItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuizzes = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/quizzes/');
      setQuizzes(response.data);
    } catch (err: any) {
      console.error('Error fetching quizzes:', err);
      const errorMessage =
        err.response?.data?.error?.message ||
        err.response?.data?.detail ||
        'Failed to load quizzes. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuizzes();
  }, []);

  return {
    quizzes,
    loading,
    error,
    refetch: fetchQuizzes,
  };
};
