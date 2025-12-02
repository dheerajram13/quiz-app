"""
Database models for quiz application.

This module defines the core domain models following Django best practices
and implementing proper constraints and validation.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    """
    Represents a category for organizing quizzes.

    Attributes:
        name: Category name
        description: Category description
        created_at: When the category was created
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Category name (max 100 characters)"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the category"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the category was created"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a tag for organizing and filtering quizzes.

    Attributes:
        name: Tag name
        created_at: When the tag was created
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Tag name (max 50 characters)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the tag was created"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return self.name


class Quiz(models.Model):
    """
    Represents a quiz containing multiple questions.

    Attributes:
        title: The quiz title
        description: Detailed description of the quiz
        created_at: Timestamp when the quiz was created
        is_active: Whether the quiz is available for users
        time_limit_minutes: Time limit in minutes (optional)
        difficulty_level: Difficulty level of the quiz
        category: Primary category for this quiz
        tags: Tags associated with this quiz
    """

    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_MEDIUM = 'medium'
    DIFFICULTY_HARD = 'hard'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Easy'),
        (DIFFICULTY_MEDIUM, 'Medium'),
        (DIFFICULTY_HARD, 'Hard'),
    ]

    title = models.CharField(
        max_length=200,
        help_text="Quiz title (max 200 characters)"
    )
    description = models.TextField(
        help_text="Detailed description of the quiz"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the quiz was created"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the quiz is available for users to take"
    )
    time_limit_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        help_text="Time limit in minutes (1-180, optional)"
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_MEDIUM,
        help_text="Difficulty level of the quiz"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quizzes',
        help_text="Primary category for this quiz"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='quizzes',
        help_text="Tags associated with this quiz"
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        """Validate the model data."""
        super().clean()
        if not self.title.strip():
            raise ValidationError({'title': 'Quiz title cannot be empty'})

    def get_total_points(self) -> int:
        """Calculate total possible points for this quiz."""
        return sum(question.points for question in self.questions.all())

    def get_question_count(self) -> int:
        """Get the number of questions in this quiz."""
        return self.questions.count()


class Question(models.Model):
    """
    Represents a question within a quiz.

    Supports multiple question types:
    - single: Single choice (radio button)
    - multi: Multiple choice (checkboxes)
    - select_words: Select specific words from text
    """

    QUESTION_TYPE_SINGLE = 'single'
    QUESTION_TYPE_MULTI = 'multi'
    QUESTION_TYPE_SELECT_WORDS = 'select_words'

    QUESTION_TYPES = [
        (QUESTION_TYPE_SINGLE, 'Single Answer'),
        (QUESTION_TYPE_MULTI, 'Multiple Answer'),
        (QUESTION_TYPE_SELECT_WORDS, 'Select Words'),
    ]

    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE,
        help_text="The quiz this question belongs to"
    )
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        help_text="Type of question"
    )
    text = models.TextField(
        help_text="The question text"
    )
    points = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Points awarded for correct answer (1-100)"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order within the quiz"
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['quiz', 'order']),
        ]

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"

    def clean(self):
        """Validate the model data."""
        super().clean()

        if not self.text.strip():
            raise ValidationError({'text': 'Question text cannot be empty'})

        # Ensure single-choice questions have exactly one correct answer
        if self.pk and self.question_type == self.QUESTION_TYPE_SINGLE:
            correct_answers = self.answers.filter(is_correct=True).count()
            if correct_answers != 1:
                raise ValidationError(
                    f'Single-choice questions must have exactly one correct answer, '
                    f'found {correct_answers}'
                )

    def get_correct_answers(self):
        """Get all correct answers for this question."""
        return self.answers.filter(is_correct=True)


class Answer(models.Model):
    """
    Represents a possible answer to a question.

    Attributes:
        question: The question this answer belongs to
        text: The answer text
        is_correct: Whether this is a correct answer
        explanation: Optional explanation for why this answer is correct/incorrect
    """

    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
        help_text="The question this answer belongs to"
    )
    text = models.CharField(
        max_length=500,
        help_text="Answer text (max 500 characters)"
    )
    is_correct = models.BooleanField(
        default=False,
        help_text="Whether this is a correct answer"
    )
    explanation = models.TextField(
        blank=True,
        help_text="Optional explanation for this answer"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order within the question"
    )

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['question', 'is_correct']),
        ]

    def __str__(self):
        correct_indicator = "✓" if self.is_correct else "✗"
        return f"{correct_indicator} {self.question.text[:30]} - {self.text[:50]}"

    def clean(self):
        """Validate the model data."""
        super().clean()

        if not self.text.strip():
            raise ValidationError({'text': 'Answer text cannot be empty'})


class UserQuizAttempt(models.Model):
    """
    Represents a user's attempt at completing a quiz.

    Tracks the score achieved, answers submitted, and when the quiz was completed.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        help_text="The user who attempted the quiz"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        help_text="The quiz that was attempted"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score as a percentage (0-100)"
    )
    answers_data = models.JSONField(
        default=dict,
        help_text="JSON data storing user's answers and correctness"
    )
    started_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the quiz was started"
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the quiz was completed"
    )
    time_taken_seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text="Time taken to complete the quiz in seconds"
    )

    class Meta:
        verbose_name = "User Quiz Attempt"
        verbose_name_plural = "User Quiz Attempts"
        ordering = ['-completed_at']
        indexes = [
            models.Index(fields=['user', '-completed_at']),
            models.Index(fields=['quiz', '-completed_at']),
            models.Index(fields=['-completed_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"

    def clean(self):
        """Validate the model data."""
        super().clean()

        if self.score < 0 or self.score > 100:
            raise ValidationError(
                {'score': f'Score must be between 0 and 100, got {self.score}'}
            )
