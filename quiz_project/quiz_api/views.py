"""
API Views for quiz application.

This module contains API viewsets that delegate business logic to services,
following the clean architecture pattern and SOLID principles.
"""

import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Quiz
from .serializers import (
    QuizSerializer,
    QuizDetailSerializer,
    QuizAnswerSubmissionSerializer,
    UserStatsSerializer,
    QuizSubmissionResponseSerializer
)
from .services import QuizService, UserStatsService
from .exceptions import QuizNotFoundException, InvalidSubmissionError

logger = logging.getLogger(__name__)


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for quiz operations.

    This viewset delegates all business logic to services,
    keeping views thin and focused on HTTP concerns only.

    Endpoints:
        GET /api/quizzes/ - List all quizzes
        GET /api/quizzes/{id}/ - Retrieve quiz details
        POST /api/quizzes/{id}/submit/ - Submit quiz answers
        GET /api/quizzes/user_stats/ - Get user statistics
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer

    @extend_schema(
        summary="List all available quizzes",
        description="Retrieve a list of all quizzes available to the authenticated user.",
        responses={200: QuizSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all available quizzes.

        Returns:
            Response with list of quizzes
        """
        logger.info(f"User {request.user.id} requested quiz list")
        quizzes = QuizService.get_all_quizzes()
        serializer = self.get_serializer(quizzes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve quiz details",
        description="Get detailed information about a specific quiz including questions and answers.",
        responses={
            200: QuizDetailSerializer,
            404: {"description": "Quiz not found"}
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed quiz information.

        Returns:
            Response with quiz details including questions
        """
        try:
            quiz = QuizService.get_quiz(kwargs.get('pk'))
            serializer = self.get_serializer(quiz)
            logger.info(f"User {request.user.id} retrieved quiz {quiz.id}")
            return Response(serializer.data)
        except QuizNotFoundException as e:
            logger.warning(f"Quiz not found: {kwargs.get('pk')}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Submit quiz answers",
        description="Submit answers for a quiz and receive calculated score.",
        request=QuizAnswerSubmissionSerializer,
        responses={
            200: QuizSubmissionResponseSerializer,
            400: {"description": "Invalid submission"},
            404: {"description": "Quiz not found"}
        },
        examples=[
            OpenApiExample(
                "Valid submission",
                value={
                    "quiz_id": 1,
                    "answers": {
                        "1": [1],
                        "2": [2, 3],
                        "3": [4]
                    }
                },
                request_only=True
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit quiz answers and calculate score.

        This endpoint validates the submission, calculates the score,
        and saves the attempt to the database.

        Args:
            request: HTTP request containing answer submission

        Returns:
            Response with score information
        """
        # Validate input
        serializer = QuizAnswerSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(
                f"Invalid submission from user {request.user.id}: {serializer.errors}"
            )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Process submission via service layer
            result = QuizService.submit_quiz(
                user=request.user,
                quiz_id=int(pk),
                submitted_answers=serializer.validated_data['answers']
            )

            logger.info(
                f"User {request.user.id} completed quiz {pk} "
                f"with score {result['score']}%"
            )

            response_serializer = QuizSubmissionResponseSerializer(result)
            return Response(response_serializer.data)

        except QuizNotFoundException as e:
            logger.error(f"Quiz not found during submission: {pk}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidSubmissionError as e:
            logger.error(f"Invalid submission for quiz {pk}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Unexpected error during quiz submission: {str(e)}")
            return Response(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get user statistics",
        description="Retrieve statistics about the authenticated user's quiz performance.",
        responses={200: UserStatsSerializer}
    )
    @action(detail=False, methods=['get'])
    def user_stats(self, request):
        """
        Get user statistics.

        Returns comprehensive statistics about the user's quiz performance
        including total quizzes taken, average score, and recent attempts.

        Returns:
            Response with user statistics
        """
        try:
            stats_service = UserStatsService(request.user)
            stats = stats_service.get_statistics()

            serializer = UserStatsSerializer(stats)
            logger.info(f"Statistics retrieved for user {request.user.id}")
            return Response(serializer.data)

        except Exception as e:
            logger.exception(f"Error retrieving stats for user {request.user.id}: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
