import { useState, useEffect } from 'react'
import { api } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

export default function Progress() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getProgress()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <WakeUpLoader message="অগ্রগতি লোড হচ্ছে" />

  if (error) return (
    <AppLayout>
      <div className="page-content">
        <div className="alert alert-danger">{error}</div>
      </div>
    </AppLayout>
  )

  if (!data) return null

  const { total_lessons, completed, in_progress, needs_revision, not_started, overall_percent } = data

  return (
    <AppLayout>
      <div className="page-content">
        <div className="page-header">
          <h1 className="page-title">📊 আমার অগ্রগতি</h1>
          <p className="page-subtitle">মোট {total_lessons}টি পাঠের মধ্যে কতটুকু শেষ।</p>
        </div>

        {/* Overall percentage */}
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="progress-circle">
            <div className="progress-num">{overall_percent}%</div>
            <p style={{ color: 'var(--text-muted)' }}>সম্পন্ন</p>
          </div>
          {/* Progress bar */}
          <div className="score-bar-track" style={{ marginTop: 16, height: 12 }}>
            <div
              className="score-bar-fill"
              style={{ width: `${overall_percent}%`, background: '#16a34a' }}
            />
          </div>
        </div>

        {/* Stats */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <StatCard icon="✅" label="সম্পন্ন" value={completed} color="#16a34a" bg="#f0fdf4" />
          <StatCard icon="📝" label="চলছে" value={in_progress} color="#1e40af" bg="#eff6ff" />
          <StatCard icon="🔄" label="সংশোধন দরকার" value={needs_revision} color="#d97706" bg="#fffbeb" />
          <StatCard icon="⏳" label="শুরু হয়নি" value={not_started} color="#64748b" bg="#f8fafc" />
        </div>

        {/* Motivation */}
        <div className="card" style={{ marginTop: 4, textAlign: 'center' }}>
          {overall_percent === 0 && <p>🚀 শুরু করো! প্রথম পাঠ তোমার জন্য অপেক্ষা করছে।</p>}
          {overall_percent > 0 && overall_percent < 50 && <p>💪 ভালো শুরু! চালিয়ে যাও।</p>}
          {overall_percent >= 50 && overall_percent < 100 && <p>🌟 অর্ধেকের বেশি শেষ! তুমি পারবে।</p>}
          {overall_percent === 100 && <p>🏆 সব পাঠ সম্পন্ন! তুমি একজন Web Developer!</p>}
        </div>
      </div>
    </AppLayout>
  )
}

function StatCard({ icon, label, value, color, bg }) {
  return (
    <div className="card" style={{ background: bg, textAlign: 'center', padding: 16 }}>
      <div style={{ fontSize: '1.5rem' }}>{icon}</div>
      <div style={{ fontSize: '1.8rem', fontWeight: 800, color, lineHeight: 1.2 }}>{value}</div>
      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 2 }}>{label}</div>
    </div>
  )
}
