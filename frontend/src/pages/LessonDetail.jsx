import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { api } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

export default function LessonDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getLesson(id)
      .then(setLesson)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <WakeUpLoader message="পাঠ লোড হচ্ছে" />

  if (error) return (
    <AppLayout>
      <div className="page-content">
        <div className="alert alert-danger">{error}</div>
        <button className="btn btn-outline btn-sm" onClick={() => navigate(-1)}>← ফিরে যাও</button>
      </div>
    </AppLayout>
  )

  if (!lesson) return null

  return (
    <AppLayout>
      <div className="page-content">
        <button className="btn btn-outline btn-sm" style={{ marginBottom: 16, width: 'auto' }} onClick={() => navigate(-1)}>
          ← ফিরে যাও
        </button>

        <div className="card" style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 8 }}>
            <span className="badge badge-blue">Day {lesson.day_number}</span>
            <span className="badge badge-green">✅ সম্পন্ন</span>
          </div>
          <h1 style={{ fontSize: '1.3rem', fontWeight: 700 }}>{lesson.title}</h1>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 4 }}>
            {lesson.stage_title} › {lesson.module_title}
          </p>
        </div>

        <div className="card">
          <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content}</ReactMarkdown>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
