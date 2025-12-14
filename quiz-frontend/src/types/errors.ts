/**
 * Error Handling Types
 * Standardized error types for the application
 */

import { AxiosError } from 'axios';

export interface ApiErrorResponse {
  error?: {
    message: string;
  };
  detail?: string;
  message?: string;
}

export type AppError = AxiosError<ApiErrorResponse>;

/**
 * Type guard to check if error is an AxiosError with our API response structure
 */
export function isApiError(error: unknown): error is AppError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'isAxiosError' in error &&
    error.isAxiosError === true
  );
}

/**
 * Extract a user-friendly error message from various error types
 */
export function getErrorMessage(error: unknown, defaultMessage = 'An unexpected error occurred'): string {
  if (isApiError(error)) {
    return (
      error.response?.data?.error?.message ||
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      defaultMessage
    );
  }

  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === 'string') {
    return error;
  }

  return defaultMessage;
}
