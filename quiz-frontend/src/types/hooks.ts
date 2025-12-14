/**
 * Custom Hook Return Types
 * Type definitions for custom React hooks
 */

import { Quiz, QuizListItem, QuizSubmitResponse, User } from './api';

export interface UseQuizResult {
  quiz: Quiz | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseQuizListResult {
  quizzes: QuizListItem[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export interface UseQuizSubmitResult {
  submitQuiz: (
    quizId: string,
    answers: Record<number, number[]>,
    startedAt: string
  ) => Promise<QuizSubmitResponse>;
  submitting: boolean;
  error: string | null;
}

export interface UseAuthResult {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}
