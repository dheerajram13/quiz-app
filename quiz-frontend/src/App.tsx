import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import QuizList from './components/QuizList';
import Quiz from './components/Quiz';
import UserStats from './components/UserStats';

const App: React.FC = () => {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/quizzes" element={isAuthenticated ? <QuizList /> : <Navigate to="/login" />} />
        <Route path="/quizzes/:id" element={isAuthenticated ? <Quiz /> : <Navigate to="/login" />} />
        <Route path="/user-stats" element={isAuthenticated ? <UserStats /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

export default App;
