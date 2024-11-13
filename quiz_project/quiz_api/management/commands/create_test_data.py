# quiz_api/management/commands/create_test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz_api.models import Quiz, Question, Answer

class Command(BaseCommand):
    help = 'Creates test data for the quiz application'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@example.com', 'testpass123')
            self.stdout.write(self.style.SUCCESS('Created test user: testuser'))

        # Create sample quizzes
        # Quiz 1: Programming Basics
        quiz1 = Quiz.objects.create(
            title="Programming Basics",
            description="Test your fundamental programming knowledge"
        )

        # Single answer questions
        q1 = Question.objects.create(
            quiz=quiz1,
            question_type='single',
            text="What does HTML stand for?",
            points=1
        )
        Answer.objects.create(question=q1, text="Hyper Text Markup Language", is_correct=True)
        Answer.objects.create(question=q1, text="High Tech Modern Language", is_correct=False)
        Answer.objects.create(question=q1, text="Hyper Transfer Markup Language", is_correct=False)

        q2 = Question.objects.create(
            quiz=quiz1,
            question_type='single',
            text="Which symbol is used for single-line comments in Python?",
            points=1
        )
        Answer.objects.create(question=q2, text="#", is_correct=True)
        Answer.objects.create(question=q2, text="//", is_correct=False)
        Answer.objects.create(question=q2, text="/*", is_correct=False)

        # Multi answer questions
        q3 = Question.objects.create(
            quiz=quiz1,
            question_type='multi',
            text="Which of these are valid Python data types?",
            points=2
        )
        Answer.objects.create(question=q3, text="int", is_correct=True)
        Answer.objects.create(question=q3, text="string", is_correct=True)
        Answer.objects.create(question=q3, text="char", is_correct=False)
        Answer.objects.create(question=q3, text="list", is_correct=True)

        # Select words question
        q4 = Question.objects.create(
            quiz=quiz1,
            question_type='select_words',
            text="Select the programming languages from this sentence: Python and JavaScript are widely used programming languages for web development.",
            points=2
        )
        Answer.objects.create(question=q4, text="Python", is_correct=True)
        Answer.objects.create(question=q4, text="JavaScript", is_correct=True)
        Answer.objects.create(question=q4, text="web", is_correct=False)
        Answer.objects.create(question=q4, text="development", is_correct=False)

        # Quiz 2: Web Development
        quiz2 = Quiz.objects.create(
            title="Web Development Basics",
            description="Test your knowledge of web development"
        )

        # Single answer question
        q5 = Question.objects.create(
            quiz=quiz2,
            question_type='single',
            text="Which tag is used for the largest heading in HTML?",
            points=1
        )
        Answer.objects.create(question=q5, text="<h1>", is_correct=True)
        Answer.objects.create(question=q5, text="<h6>", is_correct=False)
        Answer.objects.create(question=q5, text="<header>", is_correct=False)

        # Multi answer question
        q6 = Question.objects.create(
            quiz=quiz2,
            question_type='multi',
            text="Which of these are CSS positioning types?",
            points=2
        )
        Answer.objects.create(question=q6, text="relative", is_correct=True)
        Answer.objects.create(question=q6, text="absolute", is_correct=True)
        Answer.objects.create(question=q6, text="floating", is_correct=False)
        Answer.objects.create(question=q6, text="fixed", is_correct=True)

        # Select words question
        q7 = Question.objects.create(
            quiz=quiz2,
            question_type='select_words',
            text="Select the frontend frameworks from this sentence: React and Vue are popular JavaScript frameworks for building user interfaces.",
            points=2
        )
        Answer.objects.create(question=q7, text="React", is_correct=True)
        Answer.objects.create(question=q7, text="Vue", is_correct=True)
        Answer.objects.create(question=q7, text="JavaScript", is_correct=False)
        Answer.objects.create(question=q7, text="interfaces", is_correct=False)

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
        self.stdout.write(self.style.SUCCESS(f'Created {Quiz.objects.count()} quizzes'))
        self.stdout.write(self.style.SUCCESS(f'Created {Question.objects.count()} questions'))
        self.stdout.write(self.style.SUCCESS(f'Created {Answer.objects.count()} answers'))