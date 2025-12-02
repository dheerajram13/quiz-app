"""
Serializers for quiz application.

This module contains DRF serializers that handle data validation and
transformation between Python objects and JSON.
"""

from rest_framework import serializers
from .models import Quiz, Question, Answer, UserQuizAttempt, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""

    class Meta:
        model = Tag
        fields = ['id', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model."""

    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'explanation']
        extra_kwargs = {
            'is_correct': {'write_only': True},  # Don't expose correct answers to users
            'explanation': {'write_only': True}  # Don't show explanations before submission
        }


class AnswerDetailSerializer(serializers.ModelSerializer):
    """Serializer for Answer model with all details (for results view)."""

    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'explanation']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model with answers."""

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_type', 'text', 'points', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    """Basic quiz serializer for list view."""

    question_count = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'question_count',
            'time_limit_minutes', 'difficulty_level', 'category', 'tags'
        ]

    def get_question_count(self, obj) -> int:
        """Return the number of questions in the quiz."""
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    """Detailed quiz serializer including questions and answers."""

    questions = QuestionSerializer(many=True, read_only=True)
    total_points = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'questions', 'total_points',
            'time_limit_minutes', 'difficulty_level', 'category', 'tags'
        ]

    def get_total_points(self, obj) -> int:
        """Calculate total possible points for the quiz."""
        return sum(question.points for question in obj.questions.all())


class QuizAnswerSubmissionSerializer(serializers.Serializer):
    """Serializer for validating quiz answer submissions."""

    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            allow_empty=True
        ),
        help_text="Dictionary mapping question IDs to lists of answer IDs"
    )
    started_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="When the user started the quiz"
    )

    def validate_quiz_id(self, value):
        """Validate that the quiz exists."""
        try:
            Quiz.objects.get(id=value)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError(f"Quiz with ID {value} does not exist")
        return value

    def validate(self, data):
        """
        Validate the entire submission.

        Ensures that:
        - All question IDs belong to the specified quiz
        - Single-choice questions have only one answer
        - Answer IDs exist and belong to the correct question
        """
        quiz_id = data['quiz_id']
        answers = data['answers']

        # Get all questions for this quiz
        questions = Question.objects.filter(quiz_id=quiz_id).prefetch_related('answers')
        question_dict = {str(q.id): q for q in questions}

        for question_id, answer_ids in answers.items():
            # Validate question belongs to quiz
            if question_id not in question_dict:
                raise serializers.ValidationError(
                    f"Question {question_id} does not belong to quiz {quiz_id}"
                )

            question = question_dict[question_id]

            # Validate single-choice questions
            if question.question_type == 'single' and len(answer_ids) > 1:
                raise serializers.ValidationError(
                    f"Question {question_id} is single-choice but {len(answer_ids)} answers were provided"
                )

            # Validate answer IDs exist and belong to this question
            valid_answer_ids = set(
                question.answers.values_list('id', flat=True)
            )

            for answer_id in answer_ids:
                if answer_id not in valid_answer_ids:
                    raise serializers.ValidationError(
                        f"Answer {answer_id} does not belong to question {question_id}"
                    )

        return data


class QuizSubmissionResponseSerializer(serializers.Serializer):
    """Serializer for quiz submission response."""

    score = serializers.FloatField(
        help_text="Score as a percentage (0-100)"
    )
    total_points = serializers.IntegerField(
        help_text="Total possible points in the quiz"
    )
    earned_points = serializers.IntegerField(
        help_text="Points earned by the user"
    )
    percentage = serializers.FloatField(
        help_text="Score percentage (same as score, for backward compatibility)"
    )
    results = serializers.ListField(
        required=False,
        help_text="Detailed results for each question"
    )
    time_taken_seconds = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Time taken to complete the quiz in seconds"
    )


class UserQuizAttemptSerializer(serializers.ModelSerializer):
    """Serializer for user quiz attempts."""

    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    quiz_id = serializers.IntegerField(source='quiz.id', read_only=True)

    class Meta:
        model = UserQuizAttempt
        fields = ['id', 'quiz_id', 'quiz_title', 'score', 'completed_at']
        read_only_fields = ['id', 'score', 'completed_at']


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics."""

    total_quizzes = serializers.IntegerField(
        help_text="Total number of quizzes completed"
    )
    average_score = serializers.FloatField(
        help_text="Average score across all attempts"
    )
    highest_score = serializers.FloatField(
        help_text="Best score achieved"
    )
    recent_attempts = UserQuizAttemptSerializer(
        many=True,
        help_text="Most recent quiz attempts"
    )
