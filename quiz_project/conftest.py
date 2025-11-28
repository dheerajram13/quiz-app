"""
Pytest configuration and fixtures for the quiz application.
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from quiz_api.models import Quiz, Question, Answer


@pytest.fixture
def api_client():
    """Provide an API client for making requests."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Provide an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def quiz(db):
    """Create a test quiz."""
    return Quiz.objects.create(
        title='Test Quiz',
        description='A quiz for testing purposes',
        is_active=True
    )


@pytest.fixture
def question_single(quiz):
    """Create a single-choice question."""
    return Question.objects.create(
        quiz=quiz,
        question_type=Question.QUESTION_TYPE_SINGLE,
        text='What is 2 + 2?',
        points=1,
        order=1
    )


@pytest.fixture
def question_multi(quiz):
    """Create a multi-choice question."""
    return Question.objects.create(
        quiz=quiz,
        question_type=Question.QUESTION_TYPE_MULTI,
        text='Select all even numbers:',
        points=2,
        order=2
    )


@pytest.fixture
def answers_single(question_single):
    """Create answers for single-choice question."""
    answers = [
        Answer.objects.create(
            question=question_single,
            text='3',
            is_correct=False,
            order=1
        ),
        Answer.objects.create(
            question=question_single,
            text='4',
            is_correct=True,
            order=2
        ),
        Answer.objects.create(
            question=question_single,
            text='5',
            is_correct=False,
            order=3
        ),
    ]
    return answers


@pytest.fixture
def answers_multi(question_multi):
    """Create answers for multi-choice question."""
    answers = [
        Answer.objects.create(
            question=question_multi,
            text='1',
            is_correct=False,
            order=1
        ),
        Answer.objects.create(
            question=question_multi,
            text='2',
            is_correct=True,
            order=2
        ),
        Answer.objects.create(
            question=question_multi,
            text='3',
            is_correct=False,
            order=3
        ),
        Answer.objects.create(
            question=question_multi,
            text='4',
            is_correct=True,
            order=4
        ),
    ]
    return answers


@pytest.fixture
def complete_quiz(quiz, question_single, question_multi, answers_single, answers_multi):
    """Provide a complete quiz with questions and answers."""
    return quiz
