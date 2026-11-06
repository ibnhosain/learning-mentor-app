import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

const STATUS_LABEL = {
  completed:      { text: '✅ সম্পন্ন',       cls: 'badge-green' },
  in_progress:    { text: '📝 চলছে',          cls: 'badge-blue' },
  needs_revision: { text: '🔄 সংশোধন দরকার', cls: 'badge-yellow' },
  not_started:    { text: '⏳ শুরু হয়নি',     cls: 'badge-gray' },
}

export default function Modules() {
  const navigate = useNavigate()
  const [stages, setStages] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [openStage, setOpenStage] = useState(0)

  useEffect(() => {
    api.getStages()
      .then(setStages)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <WakeUpLoader message="মডিউল লোড হচ্ছে" />

  return (
    <AppLayout>
      <div className="page-content">
        <div className="page-header">
          <h1 className="page-title">📋 মডিউল সমূহ</h1>
          <p className="page-subtitle">সমস্ত পাঠের তালিকা — Stage ও Module অনুযায়ী।</p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {stages.map((stage, si) => (
          <div key={stage.id} className="card" style={{ padding: 0, overflow: 'hidden', marginBottom: 16 }}>
            {/* Stage header */}
            <button
              className="stage-header"
              onClick={() => setOpenStage(openStage === si ? -1 : si)}
            >
              <div>
                <span className="stage-num">Stage {stage.number}</span>
                <span className="stage-title"> — {stage.title}</span>
              </div>
              <span style={{ fontSize: '1.2rem' }}>{openStage === si ? '▲' : '▼'}</span>
            </button>

            {openStage === si && stage.modules?.map(mod => (
              <div key={mod.id} className="module-block">
                <div className="module-title">📦 {mod.title}</div>
                {mod.lessons?.map(lesson => {
                  const st = STATUS_LABEL[lesson.progress?.status] || STATUS_LABEL.not_started
                  return (
                    <div
                      key={lesson.id}
                      className="module-lesson-row"
                      onClick={() => lesson.progress?.status === 'completed' && navigate(`/lesson/${lesson.id}`)}
                      style={{ cursor: lesson.progress?.status === 'completed' ? 'pointer' : 'default' }}
                    >
                      <span className="module-lesson-day">Day {lesson.day_number}</span>
                      <span className="module-lesson-title">{lesson.title}</span>
                      <span className={`badge ${st.cls}`} style={{ fontSize: '0.72rem', whiteSpace: 'nowrap' }}>{st.text}</span>
                    </div>
                  )
                })}
              </div>
            ))}
          </div>
        ))}
      </div>
    </AppLayout>
  )
}
