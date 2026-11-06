import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { api } from '../api/client'
import Navbar from '../components/Navbar'
import WakeUpLoader from '../components/WakeUpLoader'

export default function TodayLesson() {
  const navigate = useNavigate()
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  useEffect(() => {
    api.getToday()
      .then(data => {
        if (data?.message) { setDone(true) }
        else { setLesson(data) }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <WakeUpLoader message="পাঠ লোড হচ্ছে" />

  if (done) return (
    <>
      <Navbar />
      <div className="app-container" style={{ paddingTop: 24 }}>
        <div className="card" style={{ textAlign: 'center', padding: 40 }}>
          <div style={{ fontSize: '3rem' }}>🏆</div>
          <h2 style={{ marginTop: 12 }}>অভিনন্দন!</h2>
          <p style={{ color: 'var(--text-muted)', marginTop: 8 }}>সব পাঠ সম্পন্ন হয়েছে।</p>
        </div>
      </div>
    </>
  )

  if (error) return (
    <>
      <Navbar />
      <div className="app-container" style={{ paddingTop: 24 }}>
        <div className="alert alert-danger">{error}</div>
        <button className="btn btn-outline" onClick={() => window.location.reload()}>আবার চেষ্টা</button>
      </div>
    </>
  )

  if (!lesson) return null

  const statusLabel = {
    not_started: { text: 'শুরু হয়নি', cls: 'badge-gray' },
    in_progress: { text: 'চলছে', cls: 'badge-blue' },
    needs_revision: { text: 'সংশোধন দরকার', cls: 'badge-yellow' },
    completed: { text: 'সম্পন্ন', cls: 'badge-green' },
  }
  const st = statusLabel[lesson.progress?.status] || statusLabel.in_progress

  return (
    <>
      <Navbar />
      <div className="app-container" style={{ paddingTop: 20 }}>

        {/* Header */}
        <div className="card" style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', marginBottom: 8 }}>
            <span className="badge badge-blue">Day {lesson.day_number}</span>
            <span className={`badge ${st.cls}`}>{st.text}</span>
          </div>
          <h1 className="page-title">{lesson.title}</h1>
          {lesson.module_title && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 4 }}>
              {lesson.stage_title} › {lesson.module_title}
            </p>
          )}
        </div>

        {/* Lesson content */}
        <div className="card">
          <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {lesson.content}
            </ReactMarkdown>
          </div>
        </div>

        {/* Submit button */}
        {lesson.progress?.status !== 'completed' && (
          <button
            className="btn btn-primary"
            onClick={() => navigate(`/submit/${lesson.id}`)}
          >
            ✍️ কাজ জমা দিন
          </button>
        )}
        {lesson.progress?.status === 'completed' && (
          <div className="alert alert-success" style={{ textAlign: 'center' }}>
            ✅ এই পাঠ সম্পন্ন হয়েছে! পরের পাঠ খুলে গেছে।
          </div>
        )}
      </div>
    </>
  )
}
