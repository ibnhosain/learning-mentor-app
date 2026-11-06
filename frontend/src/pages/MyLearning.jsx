import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

export default function MyLearning() {
  const navigate = useNavigate()
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getLessons()
      .then(data => setLessons(data.filter(l => l.progress?.status === 'completed')))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <WakeUpLoader message="লোড হচ্ছে" />

  return (
    <AppLayout>
      <div className="page-content">
        <div className="page-header">
          <h1 className="page-title">📚 আমার শেখা</h1>
          <p className="page-subtitle">তোমার সম্পন্ন করা পাঠগুলো এখানে দেখতে ও আবার পড়তে পারবে।</p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {lessons.length === 0 && !error && (
          <div className="card" style={{ textAlign: 'center', padding: 40 }}>
            <div style={{ fontSize: '3rem', marginBottom: 12 }}>📖</div>
            <p style={{ color: 'var(--text-muted)' }}>এখনো কোনো পাঠ সম্পন্ন হয়নি।</p>
            <button className="btn btn-primary btn-sm" style={{ marginTop: 16 }} onClick={() => navigate('/')}>
              আজকের পাঠ শুরু করো
            </button>
          </div>
        )}

        <div className="lesson-grid">
          {lessons.map(lesson => (
            <div
              key={lesson.id}
              className="lesson-card completed"
              onClick={() => navigate(`/lesson/${lesson.id}`)}
            >
              <div className="lesson-card-day">Day {lesson.day_number}</div>
              <div className="lesson-card-title">{lesson.title}</div>
              <div className="lesson-card-meta">
                {lesson.module_title}
                {lesson.progress?.best_score > 0 && (
                  <span className="lesson-card-score">🏆 {lesson.progress.best_score}%</span>
                )}
              </div>
              <div className="lesson-card-status badge badge-green">✅ সম্পন্ন</div>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  )
}
