import { Routes, Route, Navigate } from 'react-router-dom'
import { isLoggedIn } from './api/client'
import { AppProvider } from './context/AppContext'
import Login from './pages/Login'
import TodayLesson from './pages/TodayLesson'
import SubmitWork from './pages/SubmitWork'
import Evaluation from './pages/Evaluation'
import Progress from './pages/Progress'
import MyLearning from './pages/MyLearning'
import Modules from './pages/Modules'
import LessonDetail from './pages/LessonDetail'

function PrivateRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <AppProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<PrivateRoute><TodayLesson /></PrivateRoute>} />
        <Route path="/submit/:lessonId" element={<PrivateRoute><SubmitWork /></PrivateRoute>} />
        <Route path="/evaluation" element={<PrivateRoute><Evaluation /></PrivateRoute>} />
        <Route path="/progress" element={<PrivateRoute><Progress /></PrivateRoute>} />
        <Route path="/my-learning" element={<PrivateRoute><MyLearning /></PrivateRoute>} />
        <Route path="/modules" element={<PrivateRoute><Modules /></PrivateRoute>} />
        <Route path="/lesson/:id" element={<PrivateRoute><LessonDetail /></PrivateRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppProvider>
  )
}
