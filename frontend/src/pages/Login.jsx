import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, setTokens, isLoggedIn } from '../api/client'
import WakeUpLoader from '../components/WakeUpLoader'

export default function Login() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [installPrompt, setInstallPrompt] = useState(null)

  useEffect(() => {
    if (isLoggedIn()) navigate('/', { replace: true })

    // Android PWA install prompt ধরে রাখো
    const handler = e => { e.preventDefault(); setInstallPrompt(e) }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [navigate])

  async function handleInstall() {
    if (!installPrompt) return
    installPrompt.prompt()
    const result = await installPrompt.userChoice
    if (result.outcome === 'accepted') setInstallPrompt(null)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!username || !password) { setError('Username ও password দাও।'); return }
    setLoading(true)
    setError('')
    try {
      const data = await api.login(username, password)
      setTokens(data.access, data.refresh)
      navigate('/', { replace: true })
    } catch (err) {
      setError(err.message || 'Login ব্যর্থ হয়েছে। আবার চেষ্টা করো।')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <WakeUpLoader message="Login হচ্ছে" />

  return (
    <div className="login-page">
      <div className="login-logo">📚</div>
      <h1 className="login-title">Learning Mentor</h1>
      <p className="login-subtitle">ধাপে ধাপে Web Development শিখি</p>

      {/* Android install banner */}
      {installPrompt && (
        <div className="install-banner" style={{ width: '100%', maxWidth: 400, marginBottom: 20 }}>
          <p>📲 এই অ্যাপ মোবাইলে install করো!</p>
          <button className="btn" onClick={handleInstall}>Install করো</button>
        </div>
      )}

      {/* iOS instructions */}
      {!installPrompt && /iphone|ipad|ipod/i.test(navigator.userAgent) && (
        <div className="card" style={{ maxWidth: 400, marginBottom: 20, textAlign: 'center' }}>
          <p style={{ fontSize: '0.9rem' }}>
            📲 <strong>iPhone-এ install করতে:</strong><br />
            নিচে <strong>Share</strong> বাটন চাপো → <strong>"Add to Home Screen"</strong> বেছে নাও
          </p>
        </div>
      )}

      <div className="card login-card">
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              className="form-control"
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              autoComplete="username"
              autoCapitalize="none"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              className="form-control"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>
          <button type="submit" className="btn btn-primary">প্রবেশ করো</button>
        </form>
      </div>
    </div>
  )
}
