from rest_framework import serializers
from .models import Quiz, Question, Answer, UserQuizAttempt

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {'is_correct': {'write_only': True}}

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_type', 'text', 'points', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'

class QuizAnswerSubmissionSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )

    def validate(self, data):
        quiz_id = data['quiz_id']
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise serializers.ValidationError("Invalid quiz ID")
            
        answers = data['answers']
        for question_id, answer_ids in answers.items():
            try:
                question = Question.objects.get(id=question_id, quiz_id=quiz_id)
            except Question.DoesNotExist:
                raise serializers.ValidationError(f"Invalid question ID: {question_id}")
                
            if question.question_type == 'single' and len(answer_ids) > 1:
                raise serializers.ValidationError(
                    f"Question {question_id} is single-choice but multiple answers were provided"
                )
        
        return data

class UserQuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    
    class Meta:
        model = UserQuizAttempt
        fields = ['id', 'quiz_title', 'score', 'completed_at']

class UserStatsSerializer(serializers.Serializer):
    total_quizzes = serializers.IntegerField()
    average_score = serializers.FloatField()
    highest_score = serializers.IntegerField()
    recent_attempts = UserQuizAttemptSerializer(many=True)