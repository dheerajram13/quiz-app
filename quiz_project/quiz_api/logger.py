"""
Centralized logging utility for quiz application.

This module provides a single, consistent logger interface for the entire
application, ensuring uniform logging behavior and configuration.

Usage:
    # Import the logger in any module
    from quiz_api.logger import logger

    # Use the logger throughout your code
    logger.info("User logged in successfully")
    logger.warning("API rate limit approaching")
    logger.error("Failed to process request")
    logger.exception("An error occurred during processing")

    # Or use the class methods directly
    from quiz_api.logger import QuizAppLogger
    QuizAppLogger.info("Application started")

Features:
    - Single logger instance across the entire application
    - Configured in settings.py with rotating file handlers
    - Separate error log file for ERROR and CRITICAL level logs
    - Console and file output with different formatters
    - Automatic log rotation (10MB max size, 5 backup files)

Log Files:
    - General logs: quiz_project/logs/quiz_app.log
    - Error logs: quiz_project/logs/quiz_app_errors.log
"""

import logging
from typing import Optional


class QuizAppLogger:
    """
    Centralized logger for the Quiz Application.

    This class provides a singleton-like logger instance that can be used
    throughout the application for consistent logging behavior.
    """

    _logger: Optional[logging.Logger] = None
    _logger_name = 'quiz_api'

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Get or create the application logger.

        Returns:
            Logger instance configured for the quiz application
        """
        if cls._logger is None:
            cls._logger = logging.getLogger(cls._logger_name)
        return cls._logger

    @classmethod
    def debug(cls, message: str, *args, **kwargs):
        """Log a debug message."""
        cls.get_logger().debug(message, *args, **kwargs)

    @classmethod
    def info(cls, message: str, *args, **kwargs):
        """Log an info message."""
        cls.get_logger().info(message, *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        """Log a warning message."""
        cls.get_logger().warning(message, *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs):
        """Log an error message."""
        cls.get_logger().error(message, *args, **kwargs)

    @classmethod
    def exception(cls, message: str, *args, **kwargs):
        """Log an exception with traceback."""
        cls.get_logger().exception(message, *args, **kwargs)

    @classmethod
    def critical(cls, message: str, *args, **kwargs):
        """Log a critical message."""
        cls.get_logger().critical(message, *args, **kwargs)


# Create a convenience instance for easier imports
logger = QuizAppLogger.get_logger()
