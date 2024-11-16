# Quiz Application

This is a full-stack application consisting of a **React frontend** and a **Django backend** that allows users to take quizzes, track their progress, and manage their quiz data. The app is dockerized for easy development and deployment.

## Features

- **User Authentication**: Login and token-based authentication for accessing the quiz and user statistics.
- **Quiz Management**: List of quizzes, individual quiz pages, and tracking of user performance.
- **API Integration**: Django backend exposes RESTful API to the React frontend for handling quiz data.
- **Dockerized**: Both frontend and backend are containerized using Docker for easy setup and deployment.

## Tech Stack

- **Frontend**: React.js (with TypeScript)
- **Backend**: Django (with Python)
- **Database**: PostgreSQL
- **Docker**: Docker Compose for managing multi-container applications
- **Authentication**: Token-based authentication using local storage

## Prerequisites

To run this application locally, you need the following installed on your system:

- Docker
- Docker Compose
- Node.js (for building frontend separately if needed)
- Python (for Django backend)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/quiz-app.git
cd quiz-app


docker-compose up --build
```