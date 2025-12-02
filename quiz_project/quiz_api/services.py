"""
Service layer for quiz application.

This module implements the Service Layer pattern to separate business logic
from views, following SOLID principles (Single Responsibility Principle).
"""

import logging
from typing import Dict, List, Tuple, Optional
from decimal import Decimal
from datetime import datetime
from django.db.models import Avg, Max, QuerySet
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Quiz, Question, UserQuizAttempt
from .exceptions import QuizNotFoundException, InvalidSubmissionError
from .scoring_strategies import ScoringStrategyFactory


logger = logging.getLogger(__name__)


class QuizScoringService:
    """
    Service responsible for scoring quiz submissions.

    This class implements the Single Responsibility Principle by focusing
    solely on quiz scoring logic.
    """

    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def calculate_score(
        self,
        submitted_answers: Dict[str, List[int]],
        include_details: bool = False
    ) -> Tuple[Decimal, int, int, Optional[List[Dict]]]:
        """
        Calculate the score for a quiz submission.

        Args:
            submitted_answers: Dictionary mapping question IDs to answer IDs
            include_details: Whether to include detailed results for each question

        Returns:
            Tuple of (score_percentage, total_points, earned_points, detailed_results)

        Raises:
            InvalidSubmissionError: If the submission data is invalid
        """
        total_points = 0
        earned_points = 0
        detailed_results = [] if include_details else None

        for question in self.quiz.questions.select_related().prefetch_related('answers'):
            total_points += question.points
            question_answers = submitted_answers.get(str(question.id), [])

            is_correct = self._is_answer_correct(question, question_answers)
            points_awarded = question.points if is_correct else 0
            earned_points += points_awarded

            if is_correct:
                logger.info(
                    f"Question {question.id} answered correctly. "
                    f"Points awarded: {question.points}"
                )

            if include_details:
                correct_answer_ids = list(question.answers.filter(is_correct=True).values_list('id', flat=True))
                detailed_results.append({
                    'question_id': question.id,
                    'question_text': question.text,
                    'question_type': question.question_type,
                    'points': question.points,
                    'is_correct': is_correct,
                    'points_awarded': points_awarded,
                    'user_answer_ids': question_answers,
                    'correct_answer_ids': correct_answer_ids,
                    'answers': [
                        {
                            'id': answer.id,
                            'text': answer.text,
                            'is_correct': answer.is_correct,
                            'explanation': answer.explanation,
                            'was_selected': answer.id in question_answers
                        }
                        for answer in question.answers.all()
                    ]
                })

        score_percentage = self._calculate_percentage(earned_points, total_points)

        logger.info(
            f"Quiz {self.quiz.id} scored: {score_percentage}% "
            f"({earned_points}/{total_points} points)"
        )

        return score_percentage, total_points, earned_points, detailed_results

    def _is_answer_correct(self, question: Question, submitted_answer_ids: List[int]) -> bool:
        """
        Check if the submitted answers for a question are correct.

        Uses the Strategy Pattern to delegate scoring logic to the appropriate
        strategy based on question type.

        Args:
            question: The question being evaluated
            submitted_answer_ids: List of submitted answer IDs

        Returns:
            True if the answer is correct, False otherwise
        """
        try:
            strategy = ScoringStrategyFactory.get_strategy(question.question_type)
            return strategy.is_correct(question, submitted_answer_ids)
        except ValueError as e:
            logger.error(f"Error getting scoring strategy: {e}")
            return False

    @staticmethod
    def _calculate_percentage(earned: int, total: int) -> Decimal:
        """Calculate percentage score with proper decimal handling."""
        if total == 0:
            return Decimal('0.00')
        return Decimal((earned / total) * 100).quantize(Decimal('0.01'))


class QuizAttemptService:
    """
    Service for managing quiz attempts.

    Handles creation and retrieval of quiz attempts, implementing the
    Repository pattern abstraction.
    """

    @staticmethod
    def create_attempt(
        user: User,
        quiz: Quiz,
        score: Decimal,
        answers_data: Optional[Dict] = None,
        started_at: Optional[datetime] = None,
        time_taken_seconds: Optional[int] = None
    ) -> UserQuizAttempt:
        """
        Create a new quiz attempt record.

        Args:
            user: The user taking the quiz
            quiz: The quiz being attempted
            score: The achieved score percentage
            answers_data: Optional dictionary of submitted answers and results
            started_at: When the user started the quiz
            time_taken_seconds: Time taken to complete the quiz in seconds

        Returns:
            The created UserQuizAttempt instance
        """
        attempt = UserQuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            answers_data=answers_data or {},
            started_at=started_at or timezone.now(),
            time_taken_seconds=time_taken_seconds
        )

        logger.info(
            f"Quiz attempt created: User {user.id}, Quiz {quiz.id}, "
            f"Score {score}%, Time taken: {time_taken_seconds}s, Attempt ID {attempt.id}"
        )

        return attempt

    @staticmethod
    def get_user_attempts(user: User) -> QuerySet[UserQuizAttempt]:
        """Get all quiz attempts for a user."""
        return UserQuizAttempt.objects.filter(user=user).select_related('quiz')

    @staticmethod
    def get_recent_attempts(user: User, limit: int = 5) -> QuerySet[UserQuizAttempt]:
        """Get recent quiz attempts for a user."""
        return QuizAttemptService.get_user_attempts(user)[:limit]


class UserStatsService:
    """
    Service for calculating user statistics.

    Encapsulates all statistics-related business logic.
    """

    def __init__(self, user: User):
        self.user = user
        self._attempts = QuizAttemptService.get_user_attempts(user)

    def get_statistics(self) -> Dict:
        """
        Calculate comprehensive user statistics.

        Returns:
            Dictionary containing user statistics:
            - total_quizzes: Total number of quizzes taken
            - average_score: Average score across all attempts
            - highest_score: Best score achieved
            - lowest_score: Lowest score achieved
            - recent_attempts: Last 5 quiz attempts
            - total_time_spent: Total time spent on quizzes (if tracked)
        """
        aggregates = self._attempts.aggregate(
            avg_score=Avg('score'),
            max_score=Max('score')
        )

        stats = {
            'total_quizzes': self._attempts.count(),
            'average_score': round(aggregates['avg_score'] or 0, 2),
            'highest_score': aggregates['max_score'] or 0,
            'recent_attempts': QuizAttemptService.get_recent_attempts(self.user)
        }

        logger.info(f"Statistics calculated for user {self.user.id}: {stats}")

        return stats


class QuizService:
    """
    Main service for quiz operations.

    Coordinates between different services and acts as a facade.
    This implements the Facade pattern for simplified client interaction.
    """

    @staticmethod
    def get_quiz(quiz_id: int) -> Quiz:
        """
        Retrieve a quiz by ID.

        Args:
            quiz_id: The ID of the quiz to retrieve

        Returns:
            Quiz instance

        Raises:
            QuizNotFoundException: If quiz doesn't exist
        """
        try:
            return Quiz.objects.prefetch_related(
                'questions__answers'
            ).get(id=quiz_id)
        except Quiz.DoesNotExist:
            logger.error(f"Quiz not found: {quiz_id}")
            raise QuizNotFoundException(f"Quiz with ID {quiz_id} not found")

    @staticmethod
    def get_all_quizzes() -> QuerySet[Quiz]:
        """Retrieve all available quizzes with optimized queries."""
        return Quiz.objects.prefetch_related('questions').all()

    @staticmethod
    def submit_quiz(
        user: User,
        quiz_id: int,
        submitted_answers: Dict[str, List[int]],
        started_at: Optional[datetime] = None
    ) -> Dict:
        """
        Process a quiz submission.

        This method coordinates between QuizScoringService and QuizAttemptService
        to handle the complete submission workflow.

        Args:
            user: The user submitting the quiz
            quiz_id: ID of the quiz being submitted
            submitted_answers: Dictionary of question_id -> answer_ids
            started_at: When the user started the quiz (for time tracking)

        Returns:
            Dictionary containing score information and detailed results

        Raises:
            QuizNotFoundException: If quiz doesn't exist
            InvalidSubmissionError: If submission is invalid
        """
        # Retrieve quiz
        quiz = QuizService.get_quiz(quiz_id)

        # Calculate score with detailed results
        scoring_service = QuizScoringService(quiz)
        score, total_points, earned_points, detailed_results = scoring_service.calculate_score(
            submitted_answers,
            include_details=True
        )

        # Calculate time taken if started_at is provided
        time_taken_seconds = None
        if started_at:
            completed_at = timezone.now()
            time_taken_seconds = int((completed_at - started_at).total_seconds())

        # Save attempt with detailed data
        QuizAttemptService.create_attempt(
            user=user,
            quiz=quiz,
            score=score,
            answers_data={
                'submitted_answers': submitted_answers,
                'detailed_results': detailed_results
            },
            started_at=started_at,
            time_taken_seconds=time_taken_seconds
        )

        return {
            'score': float(score),
            'total_points': total_points,
            'earned_points': earned_points,
            'percentage': float(score),
            'results': detailed_results,
            'time_taken_seconds': time_taken_seconds
        }
