"""
Custom exceptions for quiz application.

This module defines domain-specific exceptions, making error handling
more explicit and following SOLID principles.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class QuizAppException(APIException):
    """Base exception for all quiz application exceptions."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'An error occurred in the quiz application.'
    default_code = 'quiz_app_error'


class QuizNotFoundException(QuizAppException):
    """Raised when a quiz is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Quiz not found.'
    default_code = 'quiz_not_found'


class QuestionNotFoundException(QuizAppException):
    """Raised when a question is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Question not found.'
    default_code = 'question_not_found'


class InvalidSubmissionError(QuizAppException):
    """Raised when a quiz submission is invalid."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid quiz submission.'
    default_code = 'invalid_submission'


class QuizAlreadyAttemptedException(QuizAppException):
    """Raised when a user tries to retake a quiz that doesn't allow retakes."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'This quiz has already been attempted.'
    default_code = 'quiz_already_attempted'


class InsufficientPermissionsError(QuizAppException):
    """Raised when a user doesn't have permission to perform an action."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'insufficient_permissions'


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.

    Provides consistent error response format across the API.
    """
    from rest_framework.views import exception_handler
    from .logger import logger

    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Log the exception
        logger.error(
            f"API Exception: {exc.__class__.__name__} - {str(exc)} "
            f"- View: {context.get('view', 'Unknown')} "
            f"- Request: {context.get('request', 'Unknown')}"
        )

        # Customize the response format
        custom_response = {
            'error': {
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error'),
                'status_code': response.status_code,
            }
        }

        # Add details if available
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response['error']['details'] = exc.detail
            else:
                custom_response['error']['message'] = str(exc.detail)

        response.data = custom_response

    return response
