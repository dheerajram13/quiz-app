/**
 * API Response Types
 * Centralized type definitions for API responses
 */

export interface ApiError {
  message: string;
  detail?: string;
  status?: number;
}

export interface Answer {
  id: number;
  text: string;
  is_correct?: boolean;
  explanation?: string;
  was_selected?: boolean;
}

export interface Question {
  id: number;
  text: string;
  question_type: 'single' | 'multiple';
  points: number;
  answers: Answer[];
}

export interface Category {
  id: number;
  name: string;
  description?: string;
}

export interface Tag {
  id: number;
  name: string;
}

export interface Quiz {
  id: number;
  title: string;
  description: string;
  questions: Question[];
  total_points: number;
  time_limit_minutes?: number | null;
  difficulty_level?: 'easy' | 'medium' | 'hard';
  category?: Category | null;
  tags?: Tag[];
}

export interface QuizListItem {
  id: number;
  title: string;
  description: string;
  question_count: number;
  created_at: string;
  difficulty_level?: 'easy' | 'medium' | 'hard';
  category?: Category | null;
  tags?: Tag[];
}

export interface QuestionResult {
  question_id: number;
  question_text: string;
  is_correct: boolean;
  points: number;
  points_awarded: number;
  answers: Answer[];
}

export interface QuizSubmitResponse {
  score: number;
  earned_points: number;
  total_points: number;
  time_taken_seconds?: number;
  results?: QuestionResult[];
}

export interface QuizSubmitRequest {
  answers: Record<number, number[]>;
  started_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

export interface UserStats {
  total_quizzes_taken: number;
  total_points_earned: number;
  average_score: number;
  recent_attempts?: QuizAttempt[];
}

export interface QuizAttempt {
  id: number;
  quiz_title: string;
  score: number;
  earned_points: number;
  total_points: number;
  completed_at: string;
  time_taken_seconds?: number;
}
