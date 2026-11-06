import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { api } from '../api/client'
import { useApp } from '../context/AppContext'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

export default function TodayLesson() {
  const { saveCurrentLesson } = useApp()
  const [lesson, setLesson] = useState(null)
  const [nextLesson, setNextLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  useEffect(() => {
    api.getToday()
      .then(data => {
        if (data?.message) { setDone(true); return }
        setLesson(data)
        saveCurrentLesson(data.id)
        // পরের পাঠ খোঁজো
        api.getLessons().then(all => {
          const sorted = all.sort((a, b) => a.day_number - b.day_number)
          const idx = sorted.findIndex(l => l.id === data.id)
          if (idx >= 0 && idx + 1 < sorted.length) setNextLesson(sorted[idx + 1])
        }).catch(() => {})
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <WakeUpLoader message="পাঠ লোড হচ্ছে" />

  if (done) return (
    <AppLayout>
      <div className="page-content">
        <div className="card" style={{ textAlign: 'center', padding: 48 }}>
          <div style={{ fontSize: '4rem' }}>🏆</div>
          <h2 style={{ marginTop: 12, fontSize: '1.5rem' }}>অভিনন্দন, Faridur!</h2>
          <p style={{ color: 'var(--text-muted)', marginTop: 8 }}>সমস্ত পাঠ সম্পন্ন হয়েছে। তুমি একজন Web Developer!</p>
        </div>
      </div>
    </AppLayout>
  )

  if (error) return (
    <AppLayout>
      <div className="page-content">
        <div className="alert alert-danger">{error}</div>
        <button className="btn btn-outline btn-sm" onClick={() => window.location.reload()}>আবার চেষ্টা</button>
      </div>
    </AppLayout>
  )

  if (!lesson) return null

  const statusLabel = {
    not_started:    { text: 'শুরু হয়নি',       cls: 'badge-gray' },
    in_progress:    { text: 'চলছে',             cls: 'badge-blue' },
    needs_revision: { text: 'সংশোধন দরকার',    cls: 'badge-yellow' },
    completed:      { text: 'সম্পন্ন',          cls: 'badge-green' },
  }
  const st = statusLabel[lesson.progress?.status] || statusLabel.in_progress

  return (
    <AppLayout>
      <div className="page-content">

        {/* Hero header */}
        <div className="today-hero">
          <div className="today-hero-badges">
            <span className="badge badge-blue">Day {lesson.day_number}</span>
            <span className={`badge ${st.cls}`}>{st.text}</span>
          </div>
          <h1 className="today-hero-title">{lesson.title}</h1>
          {lesson.module_title && (
            <p className="today-hero-meta">{lesson.stage_title} › {lesson.module_title}</p>
          )}
        </div>

        {/* Lesson content */}
        <div className="card">
          <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{lesson.content}</ReactMarkdown>
          </div>
        </div>

        {/* Completed message */}
        {lesson.progress?.status === 'completed' && (
          <div className="alert alert-success" style={{ textAlign: 'center', marginBottom: 16 }}>
            ✅ এই পাঠ সম্পন্ন হয়েছে! পরের পাঠ খুলে গেছে।
          </div>
        )}

        {/* Next lesson preview */}
        {nextLesson && (
          <div className="next-lesson-card">
            <div className="next-lesson-label">পরের পাঠ</div>
            <div className="next-lesson-title">
              <span className="badge badge-gray" style={{ marginRight: 8 }}>Day {nextLesson.day_number}</span>
              {nextLesson.title}
            </div>
            <div className="next-lesson-meta">{nextLesson.module_title}</div>
            {lesson.progress?.status !== 'completed' && (
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
                🔒 আজকের পাঠ সম্পন্ন করলে পরবর্তী পাঠ খুলবে।
              </p>
            )}
          </div>
        )}

      </div>
    </AppLayout>
  )
}
