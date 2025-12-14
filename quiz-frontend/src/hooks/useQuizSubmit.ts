import { useState } from 'react';
import api from '../services/api';
import { QuizSubmitResponse, QuizSubmitRequest, UseQuizSubmitResult } from '../types';
import { getErrorMessage } from '../types/errors';

export const useQuizSubmit = (): UseQuizSubmitResult => {
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const submitQuiz = async (
    quizId: string,
    answers: Record<number, number[]>,
    startedAt: string
  ): Promise<QuizSubmitResponse> => {
    try {
      setSubmitting(true);
      setError(null);

      const payload: QuizSubmitRequest = {
        answers,
        started_at: startedAt,
      };

      const response = await api.post<QuizSubmitResponse>(
        `/quizzes/${quizId}/submit/`,
        payload
      );

      return response.data;
    } catch (err: unknown) {
      console.error('Submission error:', err);
      const errorMessage = getErrorMessage(err, 'Submission failed. Please try again.');
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  return {
    submitQuiz,
    submitting,
    error,
  };
};
