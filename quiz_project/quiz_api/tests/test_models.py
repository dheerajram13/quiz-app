"""
Unit tests for quiz API models.
"""

import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from quiz_api.models import Quiz, Question, Answer, UserQuizAttempt


@pytest.mark.unit
@pytest.mark.django_db
class TestQuizModel:
    """Tests for Quiz model."""

    def test_create_quiz(self):
        """Test creating a quiz."""
        quiz = Quiz.objects.create(
            title='Python Basics',
            description='Test your Python knowledge'
        )
        assert quiz.title == 'Python Basics'
        assert quiz.is_active is True
        assert quiz.created_at is not None

    def test_quiz_str_representation(self, quiz):
        """Test string representation of quiz."""
        assert str(quiz) == quiz.title

    def test_get_total_points(self, complete_quiz):
        """Test calculating total points for quiz."""
        total = complete_quiz.get_total_points()
        assert total == 3  # 1 point + 2 points

    def test_get_question_count(self, complete_quiz):
        """Test getting question count."""
        count = complete_quiz.get_question_count()
        assert count == 2

    def test_quiz_validation_empty_title(self):
        """Test quiz validation fails with empty title."""
        quiz = Quiz(title='   ', description='Test')
        with pytest.raises(ValidationError):
            quiz.clean()


@pytest.mark.unit
@pytest.mark.django_db
class TestQuestionModel:
    """Tests for Question model."""

    def test_create_question(self, quiz):
        """Test creating a question."""
        question = Question.objects.create(
            quiz=quiz,
            question_type=Question.QUESTION_TYPE_SINGLE,
            text='What is Python?',
            points=5
        )
        assert question.quiz == quiz
        assert question.points == 5
        assert question.question_type == 'single'

    def test_question_str_representation(self, question_single):
        """Test string representation of question."""
        str_repr = str(question_single)
        assert question_single.quiz.title in str_repr

    def test_question_ordering(self, quiz):
        """Test questions are ordered correctly."""
        q1 = Question.objects.create(
            quiz=quiz, question_type='single', text='Q1', order=2
        )
        q2 = Question.objects.create(
            quiz=quiz, question_type='single', text='Q2', order=1
        )

        questions = list(Question.objects.all())
        assert questions[0] == q2  # order=1 comes first
        assert questions[1] == q1  # order=2 comes second

    def test_get_correct_answers(self, question_single, answers_single):
        """Test getting correct answers for a question."""
        correct = question_single.get_correct_answers()
        assert correct.count() == 1
        assert correct.first().text == '4'


@pytest.mark.unit
@pytest.mark.django_db
class TestAnswerModel:
    """Tests for Answer model."""

    def test_create_answer(self, question_single):
        """Test creating an answer."""
        answer = Answer.objects.create(
            question=question_single,
            text='Test answer',
            is_correct=True
        )
        assert answer.question == question_single
        assert answer.is_correct is True

    def test_answer_str_representation(self, answers_single):
        """Test string representation includes correct indicator."""
        correct_answer = answers_single[1]  # '4' is correct
        incorrect_answer = answers_single[0]  # '3' is incorrect

        assert '✓' in str(correct_answer)
        assert '✗' in str(incorrect_answer)

    def test_answer_validation_empty_text(self, question_single):
        """Test answer validation fails with empty text."""
        answer = Answer(question=question_single, text='   ')
        with pytest.raises(ValidationError):
            answer.clean()


@pytest.mark.unit
@pytest.mark.django_db
class TestUserQuizAttemptModel:
    """Tests for UserQuizAttempt model."""

    def test_create_attempt(self, user, quiz):
        """Test creating a quiz attempt."""
        attempt = UserQuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=Decimal('85.50')
        )
        assert attempt.user == user
        assert attempt.quiz == quiz
        assert attempt.score == Decimal('85.50')
        assert attempt.completed_at is not None

    def test_attempt_str_representation(self, user, quiz):
        """Test string representation of attempt."""
        attempt = UserQuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=Decimal('90.00')
        )
        str_repr = str(attempt)
        assert user.username in str_repr
        assert quiz.title in str_repr
        assert '90' in str_repr

    def test_attempt_ordering(self, user, quiz):
        """Test attempts are ordered by completion time (newest first)."""
        attempt1 = UserQuizAttempt.objects.create(
            user=user, quiz=quiz, score=Decimal('80.00')
        )
        attempt2 = UserQuizAttempt.objects.create(
            user=user, quiz=quiz, score=Decimal('90.00')
        )

        attempts = list(UserQuizAttempt.objects.all())
        assert attempts[0] == attempt2  # Newest first
        assert attempts[1] == attempt1

    def test_attempt_validation_invalid_score(self, user, quiz):
        """Test attempt validation fails with invalid score."""
        attempt = UserQuizAttempt(
            user=user,
            quiz=quiz,
            score=Decimal('150.00')  # Invalid: > 100
        )
        with pytest.raises(ValidationError):
            attempt.clean()
