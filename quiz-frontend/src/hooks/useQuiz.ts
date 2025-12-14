import { useState, useEffect } from 'react';
import api from '../services/api';
import { Quiz, UseQuizResult } from '../types';
import { getErrorMessage } from '../types/errors';

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
      const response = await api.get<Quiz>(`/quizzes/${quizId}/`);
      setQuiz(response.data);
    } catch (err: unknown) {
      console.error('Error fetching quiz:', err);
      setError(getErrorMessage(err, 'Failed to load quiz. Please try again.'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuiz();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [quizId]);

  return {
    quiz,
    loading,
    error,
    refetch: fetchQuiz,
  };
};
