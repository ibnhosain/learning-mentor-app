import { useLocation, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'

const SCORE_LABELS = {
  concept: 'ধারণা বোঝা (২০%)',
  independent_coding: 'নিজে code করা (৩০%)',
  debugging: 'সমস্যা সমাধান (২০%)',
  project_quality: 'কোডের মান (২০%)',
  explanation: 'নিজের ব্যাখ্যা (১০%)',
}

const MAX_SCORES = { concept: 20, independent_coding: 30, debugging: 20, project_quality: 20, explanation: 10 }

function ScoreBar({ label, value, max }) {
  const pct = max > 0 ? (value / max) * 100 : 0
  const color = pct >= 75 ? '#16a34a' : pct >= 50 ? '#d97706' : '#dc2626'
  return (
    <div className="score-bar">
      <div className="score-bar-label">
        <span>{label}</span>
        <span style={{ fontWeight: 700 }}>{value}/{max}</span>
      </div>
      <div className="score-bar-track">
        <div className="score-bar-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
    </div>
  )
}

export default function Evaluation() {
  const location = useLocation()
  const navigate = useNavigate()
  const evaluation = location.state?.evaluation

  if (!evaluation) {
    return (
      <>
        <Navbar />
        <div className="app-container" style={{ paddingTop: 24 }}>
          <div className="alert alert-danger">মূল্যায়নের তথ্য পাওয়া যায়নি।</div>
          <button className="btn btn-outline" onClick={() => navigate('/')}>হোমে যাও</button>
        </div>
      </>
    )
  }

  const { scores = {}, total_score = 0, what_is_correct = [], what_is_wrong = [], hints = [], next_step = '', status = '' } = evaluation
  const passed = status === 'Completed' && total_score >= 75
  const scoreClass = passed ? 'pass' : total_score >= 50 ? 'partial' : 'fail'

  return (
    <>
      <Navbar />
      <div className="app-container" style={{ paddingTop: 20 }}>
        <p className="page-title">AI মূল্যায়নের ফলাফল</p>

        {/* Total score */}
        <div className={`score-total ${scoreClass}`}>
          <div className="num">{total_score}<span style={{ fontSize: '1.5rem' }}>/100</span></div>
          <div style={{ marginTop: 8 }}>
            {passed
              ? <span className="badge badge-green">✅ উত্তীর্ণ — পরের পাঠ খুলেছে!</span>
              : <span className={`badge ${scoreClass === 'partial' ? 'badge-yellow' : 'badge-red'}`}>
                  {status === 'Needs Revision' ? '🔄 সংশোধন দরকার' : '📝 চলছে'}
                </span>
            }
          </div>
        </div>

        {/* Score breakdown */}
        <div className="card">
          <h3 style={{ marginBottom: 14, fontSize: '1rem' }}>নম্বরের বিভাজন</h3>
          {Object.entries(SCORE_LABELS).map(([key, label]) => (
            <ScoreBar key={key} label={label} value={scores[key] ?? 0} max={MAX_SCORES[key]} />
          ))}
        </div>

        {/* What's correct */}
        {what_is_correct.length > 0 && (
          <div className="card">
            <h3 style={{ marginBottom: 10, fontSize: '1rem', color: '#15803d' }}>✅ কী ঠিক হয়েছে</h3>
            <ul className="feedback-list correct">
              {what_is_correct.map((item, i) => <li key={i}>✓ {item}</li>)}
            </ul>
          </div>
        )}

        {/* What's wrong */}
        {what_is_wrong.length > 0 && (
          <div className="card">
            <h3 style={{ marginBottom: 10, fontSize: '1rem', color: '#b91c1c' }}>❌ কী ঠিক হয়নি</h3>
            <ul className="feedback-list wrong">
              {what_is_wrong.map((item, i) => <li key={i}>✗ {item}</li>)}
            </ul>
          </div>
        )}

        {/* Hints */}
        {hints.length > 0 && (
          <div className="card">
            <h3 style={{ marginBottom: 10, fontSize: '1rem', color: '#92400e' }}>💡 Hint</h3>
            <ul className="feedback-list hint">
              {hints.map((item, i) => <li key={i}>→ {item}</li>)}
            </ul>
          </div>
        )}

        {/* Next step */}
        {next_step && (
          <div className="card">
            <h3 style={{ marginBottom: 8, fontSize: '1rem' }}>⏭️ পরের পদক্ষেপ</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>{next_step}</p>
          </div>
        )}

        {/* Actions */}
        {passed ? (
          <button className="btn btn-success" onClick={() => navigate('/')}>
            পরের পাঠ দেখো →
          </button>
        ) : (
          <button className="btn btn-primary" onClick={() => navigate(-1)}>
            🔄 আবার চেষ্টা করো
          </button>
        )}
      </div>
    </>
  )
}
