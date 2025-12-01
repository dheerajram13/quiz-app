# Quiz Application

[![CI/CD Pipeline](https://github.com/yourusername/quiz-app/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yourusername/quiz-app/actions)
[![codecov](https://codecov.io/gh/yourusername/quiz-app/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/quiz-app)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, full-stack quiz application built with **Django REST Framework** and **React TypeScript**, demonstrating best practices in software engineering including **SOLID principles**, **design patterns**, and **clean architecture**.

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Design Patterns & Principles](#-design-patterns--principles)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Code Quality](#-code-quality)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- **User Authentication**: JWT-based authentication with automatic token refresh
- **Quiz Management**: Create, retrieve, and manage quizzes through a RESTful API
- **Multiple Question Types**:
  - Single-choice (radio buttons)
  - Multiple-choice (checkboxes)
  - Select-words (keyword identification)
- **Automatic Scoring**: Server-side answer validation and percentage-based scoring
- **Performance Tracking**: User statistics including average scores, total quizzes, and attempt history
- **Responsive UI**: Material-UI based interface optimized for all devices

### Technical Excellence
- **Clean Architecture**: Separation of concerns with distinct layers (Presentation, Business Logic, Data Access)
- **Service Layer Pattern**: Business logic isolated in dedicated service classes
- **Comprehensive Testing**: Unit and integration tests with 80%+ code coverage
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Type Safety**: TypeScript frontend with strict type checking
- **Logging & Monitoring**: Structured logging for debugging and audit trails
- **Containerization**: Docker and Docker Compose for easy deployment

---

## 🏗️ System Architecture

The application follows **Clean Architecture** principles with clear separation between layers:

![System Architecture](Architecture.png)

### Architecture Layers

1. **Client Layer** (React + TypeScript)
   - React components with Material-UI
   - JWT authentication management
   - API client with interceptors

2. **API Gateway Layer** (Django REST Framework)
   - ViewSets for HTTP handling
   - JWT authentication and permissions
   - Request/response serialization

3. **Business Logic Layer** (Service Pattern)
   - `QuizService`: Quiz retrieval and submission coordination
   - `QuizScoringService`: Answer validation and score calculation
   - `UserStatsService`: Statistics aggregation
   - `QuizAttemptService`: Attempt management

4. **Data Access Layer** (Django ORM)
   - Models: `Quiz`, `Question`, `Answer`, `UserQuizAttempt`
   - Database abstraction with ORM
   - Query optimization with select_related/prefetch_related

5. **Database Layer**
   - PostgreSQL (production) / SQLite (development)
   - Indexed fields for performance
   - Data integrity constraints

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Programming language |
| **Django** | 4.2.7 | Web framework |
| **Django REST Framework** | 3.14.0 | REST API framework |
| **djangorestframework-simplejwt** | 5.3.1 | JWT authentication |
| **PostgreSQL** | 13 | Production database |
| **drf-spectacular** | 0.27.2 | API documentation |
| **pytest** | 7.4.3 | Testing framework |
| **black** | 23.12.1 | Code formatter |
| **mypy** | 1.7.1 | Static type checker |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.3.1 | UI framework |
| **TypeScript** | 4.9.5 | Type-safe JavaScript |
| **Material-UI** | 6.1.6 | Component library |
| **Axios** | 1.7.7 | HTTP client |
| **React Router** | 6.28.0 | Client-side routing |

### DevOps
- **Docker** & **Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **pytest-cov** - Code coverage reporting

---

## 🎯 Design Patterns & Principles

### SOLID Principles

#### Single Responsibility Principle (SRP)
- Each service class has one specific responsibility
- `QuizScoringService` only handles scoring logic
- `UserStatsService` only handles statistics calculation
- Views only handle HTTP concerns, delegating business logic to services

#### Open/Closed Principle (OCP)
- Services are open for extension through inheritance
- Question types can be extended without modifying existing code
- Serializers can be composed to create new representations

#### Liskov Substitution Principle (LSP)
- All service classes can be substituted where their interfaces are expected
- Exception hierarchy allows for polymorphic error handling

#### Interface Segregation Principle (ISP)
- Small, focused serializer classes instead of one large serializer
- Separate serializers for different views (list vs. detail)

#### Dependency Inversion Principle (DIP)
- Views depend on service abstractions, not concrete implementations
- Services depend on Django ORM abstraction, not direct database access

### Design Patterns Implemented

#### 1. Service Layer Pattern
```python
# Business logic isolated in services
class QuizService:
    @staticmethod
    def submit_quiz(user, quiz_id, answers):
        quiz = QuizService.get_quiz(quiz_id)
        scoring_service = QuizScoringService(quiz)
        score = scoring_service.calculate_score(answers)
        QuizAttemptService.create_attempt(user, quiz, score)
```

#### 2. Repository Pattern
```python
# Data access abstraction
class QuizAttemptService:
    @staticmethod
    def get_user_attempts(user):
        return UserQuizAttempt.objects.filter(user=user)
```

#### 3. Facade Pattern
```python
# QuizService provides simplified interface to complex subsystems
QuizService.submit_quiz()  # Coordinates multiple services
```

#### 4. Strategy Pattern
```python
# Different scoring strategies for different question types
def _is_answer_correct(self, question, submitted_answers):
    if question.question_type == 'single':
        return self._score_single_choice(...)
    elif question.question_type == 'multi':
        return self._score_multiple_choice(...)
```

---

## 📁 Project Structure

```
quiz-app/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD pipeline
├── docs/
│   └── architecture.svg           # System architecture diagram
├── quiz-frontend/                 # React TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── Login.tsx
│   │   │   ├── QuizList.tsx
│   │   │   ├── Quiz.tsx
│   │   │   └── UserStats.tsx
│   │   ├── services/
│   │   │   └── api.tsx          # Axios API client
│   │   ├── App.tsx              # Main app component
│   │   └── index.tsx            # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── quiz_project/                  # Django backend
│   ├── quiz_api/                 # Main application
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── create_test_data.py
│   │   ├── migrations/
│   │   ├── tests/               # Test suite
│   │   │   ├── test_models.py
│   │   │   ├── test_services.py
│   │   │   └── test_views.py
│   │   ├── models.py            # Domain models
│   │   ├── services.py          # Business logic layer
│   │   ├── views.py             # API views
│   │   ├── serializers.py       # DRF serializers
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── admin.py             # Django admin
│   ├── quiz_project/
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # URL routing
│   │   └── wsgi.py
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── pyproject.toml          # Black, isort, mypy config
│   ├── .flake8                 # Flake8 configuration
│   └── Dockerfile
├── docker-compose.yml           # Multi-container orchestration
└── README.md
```

---

## 📸 Screenshots

### Home Page
![Home Page after login](images/Home.png)
*Clean and modern login interface with gradient design*

### Quiz Selection
![Quiz Selection](images/Quiz.png)
*Browse available quizzes with card-based layout*

### Quiz Completion
![Quiz Completion](images/Quiz%20Completion.png)
*Interactive quiz interface with real-time answer tracking and beautiful completion modal*

### User Statistics
![User Statistics](images/User%20Statistics.png)
*Comprehensive dashboard showing performance metrics and achievement badges*

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9 or higher
- **Node.js** 16 or higher
- **Docker** & **Docker Compose** (optional, for containerized deployment)
- **PostgreSQL** 13+ (for production)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quiz-app.git
   cd quiz-app
   ```

2. **Build and start containers**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - API Documentation: http://localhost:8000/api/docs/
   - Admin Panel: http://localhost:8000/admin/

4. **Create test data**
   ```bash
   docker-compose exec backend python manage.py create_test_data
   ```

   **Test credentials**: `testuser` / `testpass123`

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd quiz_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create test data**
   ```bash
   python manage.py create_test_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd quiz-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Access application**
   - Open http://localhost:3000 in your browser

---

## 📚 API Documentation

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Quick API Reference

#### Authentication

```bash
# Obtain JWT tokens
POST /api/token/
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpass123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Refresh access token
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Quizzes

```bash
# List all quizzes
GET /api/quizzes/
Authorization: Bearer <access_token>

# Get quiz details
GET /api/quizzes/{id}/
Authorization: Bearer <access_token>

# Submit quiz answers
POST /api/quizzes/{id}/submit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quiz_id": 1,
  "answers": {
    "1": [2],        # Question 1: Answer ID 2
    "2": [3, 5],     # Question 2: Answer IDs 3 and 5
    "3": [7]
  }
}

# Get user statistics
GET /api/quizzes/user_stats/
Authorization: Bearer <access_token>
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests with coverage
cd quiz_project
pytest

# Run specific test file
pytest quiz_api/tests/test_models.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=quiz_api --cov-report=html
```

### Test Coverage

The project maintains **80%+ test coverage** including:
- Unit tests for models, serializers, and services
- Integration tests for API endpoints
- Edge case and validation tests

### Test Structure

```python
# Example: Service layer test
@pytest.mark.unit
def test_quiz_scoring_service(complete_quiz):
    service = QuizScoringService(complete_quiz)
    score, total, earned = service.calculate_score({
        '1': [2],  # Correct
        '2': [3, 5]  # Partially correct
    })
    assert score > 0
    assert earned <= total
```

---

## 🎨 Code Quality

### Code Formatting

```bash
# Format code with Black
black quiz_api/ quiz_project/

# Sort imports with isort
isort quiz_api/ quiz_project/

# Check linting with flake8
flake8 quiz_api/ quiz_project/

# Type checking with mypy
mypy quiz_api/
```

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Code Quality Standards

- **Line length**: 100 characters
- **Code style**: Black
- **Import sorting**: isort with Black profile
- **Type hints**: mypy strict mode
- **Linting**: flake8 with max complexity 10
- **Docstrings**: Google style

---

## 🐳 Deployment

### Docker Deployment

The application includes production-ready Docker configuration:

```yaml
# docker-compose.yml includes:
- Frontend (React build with nginx)
- Backend (Django with gunicorn)
- PostgreSQL database
- Persistent volumes
- Network isolation
```

### Environment Variables

Create a `.env` file in the `quiz_project` directory:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/quizdb
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL database
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up static file serving
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Regular backups

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Format code (`black` and `isort`)
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request


---



## 🙏 Acknowledgments

- Django REST Framework community
- React and TypeScript communities
- All contributors and maintainers

---



