import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg, Count, Max
from .models import Quiz, Question, Answer, UserQuizAttempt
from .serializers import (
    QuizSerializer,
    QuizAnswerSubmissionSerializer,
    UserQuizAttemptSerializer,
    UserStatsSerializer
)

logger = logging.getLogger(__name__)

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("request", request.data)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        serializer = QuizAnswerSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        quiz = self.get_object()
        submitted_answers = serializer.validated_data['answers']
        total_points = 0
        earned_points = 0
        
        for question in quiz.questions.all():
            total_points += question.points
            question_answers = submitted_answers.get(str(question.id), [])
            
            if question.question_type == 'single':
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer and correct_answer.id in question_answers:
                    earned_points += question.points
                    
            elif question.question_type == 'multi':
                correct_answers = set(question.answers.filter(is_correct=True)
                                   .values_list('id', flat=True))
                if set(question_answers) == correct_answers:
                    earned_points += question.points
                    
            elif question.question_type == 'select_words':
                # For select_words, we'll check if all correct words are selected
                # regardless of order
                correct_answers = set(question.answers.filter(is_correct=True)
                                   .values_list('id', flat=True))
                if set(question_answers) == correct_answers:
                    earned_points += question.points

        score_percentage = (earned_points / total_points) * 100 if total_points > 0 else 0
        
        # Save the attempt
        UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score_percentage
        )
        
        return Response({
            'score': score_percentage,
            'total_points': total_points,
            'earned_points': earned_points
        })

    @action(detail=False)
    def user_stats(self, request):
        user_attempts = UserQuizAttempt.objects.filter(user=request.user)
        stats = {
            'total_quizzes': user_attempts.count(),
            'average_score': user_attempts.aggregate(Avg('score'))['score__avg'] or 0,
            'highest_score': user_attempts.aggregate(Max('score'))['score__max'] or 0,
            'recent_attempts': user_attempts[:5]
        }
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)