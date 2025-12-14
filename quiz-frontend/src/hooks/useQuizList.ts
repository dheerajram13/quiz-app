import { useState, useEffect } from 'react';
import api from '../services/api';
import { QuizListItem, UseQuizListResult } from '../types';
import { getErrorMessage } from '../types/errors';

export const useQuizList = (): UseQuizListResult => {
  const [quizzes, setQuizzes] = useState<QuizListItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuizzes = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get<QuizListItem[]>('/quizzes/');
      setQuizzes(response.data);
    } catch (err: unknown) {
      console.error('Error fetching quizzes:', err);
      setError(getErrorMessage(err, 'Failed to load quizzes. Please try again.'));
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
