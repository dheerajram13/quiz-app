import { useState } from 'react';
import api from '../services/api';

interface SubmitResponse {
  score: number;
  total_points: number;
  earned_points: number;
  percentage: number;
  results?: any[];
  time_taken_seconds?: number;
}

interface UseQuizSubmitResult {
  submitQuiz: (quizId: string, answers: Record<number, number[]>, startedAt?: string) => Promise<SubmitResponse>;
  submitting: boolean;
  error: string | null;
  result: SubmitResponse | null;
}

export const useQuizSubmit = (): UseQuizSubmitResult => {
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SubmitResponse | null>(null);

  const submitQuiz = async (
    quizId: string,
    answers: Record<number, number[]>,
    startedAt?: string
  ): Promise<SubmitResponse> => {
    try {
      setSubmitting(true);
      setError(null);
      const payload: any = {
        quiz_id: quizId,
        answers,
      };
      if (startedAt) {
        payload.started_at = startedAt;
      }
      const response = await api.post(`/quizzes/${quizId}/submit/`, payload);
      setResult(response.data);
      return response.data;
    } catch (err: any) {
      console.error('Submission error:', err);
      const errorMessage =
        err.response?.data?.error?.message ||
        err.response?.data?.detail ||
        'Submission failed. Please try again.';
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
    result,
  };
};
