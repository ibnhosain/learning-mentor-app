import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import Navbar from '../components/Navbar'
import WakeUpLoader from '../components/WakeUpLoader'

export default function SubmitWork() {
  const { lessonId } = useParams()
  const navigate = useNavigate()
  const [code, setCode] = useState('')
  const [explanation, setExplanation] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    if (!code.trim()) { setError('Code লিখতে হবে।'); return }
    if (!explanation.trim()) { setError('নিজের ভাষায় ব্যাখ্যা লিখতে হবে।'); return }
    setLoading(true)
    setError('')
    try {
      const evaluation = await api.submitWork(lessonId, code, explanation)
      navigate('/evaluation', { state: { evaluation } })
    } catch (err) {
      setError(err.message || 'জমা দেওয়া যায়নি। আবার চেষ্টা করো।')
      setLoading(false)
    }
  }

  if (loading) return <WakeUpLoader message="AI মূল্যায়ন করছে" />

  return (
    <>
      <Navbar />
      <div className="app-container" style={{ paddingTop: 20 }}>
        <p className="page-title">কাজ জমা দাও</p>
        <p className="page-subtitle">তোমার code ও ব্যাখ্যা লেখো, AI মূল্যায়ন করবে।</p>

        {/* Privacy warning */}
        <div className="alert alert-warning">
          ⚠️ <strong>সতর্কতা:</strong> কোনো password, API key বা ব্যক্তিগত তথ্য জমা দেবে না। Google Gemini free tier তোমার content দেখতে পারে।
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Code editor */}
          <div className="card">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">তোমার Code</label>
              <textarea
                className="form-control code-editor"
                value={code}
                onChange={e => setCode(e.target.value)}
                placeholder={'<!DOCTYPE html>\n<html>\n  ...\n</html>'}
                spellCheck={false}
              />
            </div>
          </div>

          {/* Live HTML Preview */}
          {code.trim() && (
            <div className="card">
              <label className="form-label">🔍 Live Preview</label>
              <iframe
                className="preview-frame"
                srcDoc={code}
                sandbox="allow-scripts"
                title="HTML Preview"
              />
            </div>
          )}

          {/* Explanation */}
          <div className="card">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">তোমার নিজের ব্যাখ্যা (২–৩ লাইন)</label>
              <textarea
                className="form-control"
                value={explanation}
                onChange={e => setExplanation(e.target.value)}
                placeholder="এই code-এ আমি কী করেছি এবং কীভাবে কাজ করে..."
                rows={4}
              />
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
                নিজের ভাষায় বোঝানো ছাড়া পূর্ণ নম্বর পাবে না।
              </p>
            </div>
          </div>

          <button type="submit" className="btn btn-primary">
            🚀 AI মূল্যায়নের জন্য জমা দাও
          </button>
        </form>

        <button
          className="btn btn-outline"
          style={{ marginTop: 12 }}
          onClick={() => navigate(-1)}
        >
          ← ফিরে যাও
        </button>
      </div>
    </>
  )
}
