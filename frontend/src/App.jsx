import { Routes, Route, Navigate } from 'react-router-dom'
import { isLoggedIn } from './api/client'
import Login from './pages/Login'
import TodayLesson from './pages/TodayLesson'
import SubmitWork from './pages/SubmitWork'
import Evaluation from './pages/Evaluation'
import Progress from './pages/Progress'

function PrivateRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<PrivateRoute><TodayLesson /></PrivateRoute>} />
      <Route path="/submit/:lessonId" element={<PrivateRoute><SubmitWork /></PrivateRoute>} />
      <Route path="/evaluation" element={<PrivateRoute><Evaluation /></PrivateRoute>} />
      <Route path="/progress" element={<PrivateRoute><Progress /></PrivateRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
