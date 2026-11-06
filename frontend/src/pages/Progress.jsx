import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, getToken } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'

const BASE_URL = import.meta.env.VITE_API_URL || 'https://learning-mentor-app.onrender.com'

export default function Progress() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [generating, setGenerating] = useState(false)
  const [logMsg, setLogMsg] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.getProgress()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function generateAndDownload() {
    setGenerating(true)
    setLogMsg('')
    try {
      // AI দিয়ে log তৈরি করো
      await fetch(`${BASE_URL}/api/daily-log/generate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` },
        body: JSON.stringify({}),
      })
      // Download করো
      const a = document.createElement('a')
      a.href = `${BASE_URL}/api/daily-log/generate/?token=${getToken()}`
      // Download directly via fetch to include auth header
      const res = await fetch(`${BASE_URL}/api/daily-log/generate/`, {
        headers: { 'Authorization': `Bearer ${getToken()}` },
      })
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      a.href = url
      a.download = `daily-log-${new Date().toISOString().slice(0, 10)}.md`
      a.click()
      URL.revokeObjectURL(url)
      setLogMsg('✅ রিপোর্ট download হয়েছে!')
    } catch {
      setLogMsg('❌ রিপোর্ট তৈরি করা যায়নি।')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) return <WakeUpLoader message="অগ্রগতি লোড হচ্ছে" />

  if (error) return (
    <AppLayout>
      <div className="page-content">
        <div className="alert alert-danger">{error}</div>
      </div>
    </AppLayout>
  )

  if (!data) return null

  const { total_lessons, completed, in_progress, needs_revision, not_started, overall_percent, weak_lessons = [] } = data

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

        {/* Weakness / needs revision list */}
        {weak_lessons.length > 0 && (
          <div className="card">
            <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 12, color: '#d97706' }}>
              🔄 সংশোধন দরকার — এই পাঠগুলো আবার চেষ্টা করো
            </h2>
            {weak_lessons.map(l => (
              <div
                key={l.id}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '10px 0', borderBottom: '1px solid var(--border)',
                }}
              >
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                    Day {l.day_number}: {l.title}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    সর্বোচ্চ score: {l.best_score}% | চেষ্টা: {l.attempts}বার
                  </div>
                </div>
                <button
                  className="btn btn-outline"
                  style={{ fontSize: '0.8rem', padding: '6px 12px' }}
                  onClick={() => navigate(`/submit/${l.id}`)}
                >
                  আবার চেষ্টা
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Daily Report Download */}
        <div className="card" style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 8 }}>📥 Daily Report</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 12 }}>
            আজকের শেখার সারসংক্ষেপ AI দিয়ে তৈরি করে Markdown ফাইলে download করো।
          </p>
          <button
            className="btn btn-primary"
            onClick={generateAndDownload}
            disabled={generating}
          >
            {generating ? '⏳ তৈরি হচ্ছে…' : '📥 আজকের Report Download করো'}
          </button>
          {logMsg && (
            <p style={{ marginTop: 8, fontSize: '0.85rem', color: logMsg.startsWith('✅') ? '#16a34a' : '#dc2626' }}>
              {logMsg}
            </p>
          )}
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
