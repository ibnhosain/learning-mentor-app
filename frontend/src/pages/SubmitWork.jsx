import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import AppLayout from '../components/AppLayout'
import WakeUpLoader from '../components/WakeUpLoader'
import CodeEditor from '../components/CodeEditor'

export default function SubmitWork() {
  const { lessonId } = useParams()
  const navigate = useNavigate()

  const [tab, setTab] = useState('code') // 'code' | 'zip'

  // code tab state
  const [code, setCode] = useState('')

  // zip tab state
  const [zipFile, setZipFile] = useState(null)

  const [explanation, setExplanation] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!explanation.trim()) {
      setError('নিজের ভাষায় ব্যাখ্যা লিখতে হবে।')
      return
    }

    if (tab === 'code') {
      if (!code.trim()) { setError('Code লিখতে হবে।'); return }
      setLoading(true)
      try {
        const evaluation = await api.submitWork(lessonId, code, explanation)
        navigate('/evaluation', { state: { evaluation } })
      } catch (err) {
        setError(err.message || 'জমা দেওয়া যায়নি।')
        setLoading(false)
      }
    } else {
      if (!zipFile) { setError('ZIP ফাইল বেছে নাও।'); return }
      setLoading(true)
      try {
        const evaluation = await api.submitZip(lessonId, zipFile, explanation)
        navigate('/evaluation', { state: { evaluation } })
      } catch (err) {
        setError(err.message || 'জমা দেওয়া যায়নি।')
        setLoading(false)
      }
    }
  }

  if (loading) return <WakeUpLoader message="AI মূল্যায়ন করছে, একটু অপেক্ষা করো…" />

  return (
    <AppLayout>
      <div className="page-content">
        <div className="page-header">
          <h1 className="page-title">✍️ কাজ জমা দাও</h1>
          <p className="page-subtitle">তোমার code ও ব্যাখ্যা দাও, AI মূল্যায়ন করবে।</p>
        </div>

        {/* Privacy warning */}
        <div className="alert alert-warning">
          ⚠️ <strong>সতর্কতা:</strong> কোনো password, API key বা ব্যক্তিগত তথ্য জমা দেবে না। Google Gemini free tier তোমার content দেখতে পারে।
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {/* Tab switcher */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <button
            className={`btn ${tab === 'code' ? 'btn-primary' : 'btn-outline'}`}
            style={{ flex: 1 }}
            onClick={() => setTab('code')}
            type="button"
          >
            ✏️ Code লিখে জমা
          </button>
          <button
            className={`btn ${tab === 'zip' ? 'btn-primary' : 'btn-outline'}`}
            style={{ flex: 1 }}
            onClick={() => setTab('zip')}
            type="button"
          >
            📁 ZIP ফাইল জমা
          </button>
        </div>

        <form onSubmit={handleSubmit}>

          {/* ── CODE TAB ── */}
          {tab === 'code' && (
            <>
              <div className="card">
                <label className="form-label" style={{ marginBottom: 8, display: 'block' }}>
                  তোমার Code
                </label>
                <CodeEditor
                  value={code}
                  onChange={setCode}
                  lang="html"
                  height="340px"
                />
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
            </>
          )}

          {/* ── ZIP TAB ── */}
          {tab === 'zip' && (
            <div className="card">
              <label className="form-label">ZIP ফাইল আপলোড করো</label>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 12 }}>
                তোমার project folder টি ZIP করে এখানে দাও। ভেতরে .html, .css, .js ফাইল থাকলে AI পড়বে।
                সর্বোচ্চ ৫ MB।
              </p>
              <input
                type="file"
                accept=".zip"
                className="form-control"
                onChange={e => setZipFile(e.target.files[0] || null)}
              />
              {zipFile && (
                <p style={{ marginTop: 8, fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  ✅ বেছে নেওয়া হয়েছে: {zipFile.name} ({(zipFile.size / 1024).toFixed(1)} KB)
                </p>
              )}
            </div>
          )}

          {/* Explanation — always shown */}
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
          type="button"
        >
          ← ফিরে যাও
        </button>
      </div>
    </AppLayout>
  )
}
