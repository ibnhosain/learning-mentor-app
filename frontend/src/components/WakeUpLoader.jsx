import { useEffect, useState } from 'react'

export default function WakeUpLoader({ message = 'লোড হচ্ছে' }) {
  const [seconds, setSeconds] = useState(0)
  const isWaking = seconds > 5

  useEffect(() => {
    const t = setInterval(() => setSeconds(s => s + 1), 1000)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="wake-loader">
      <div className="spinner" />
      {isWaking ? (
        <>
          <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>
            সার্ভার জাগছে<span className="dots" />
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            প্রথমবার একটু সময় লাগে (~১ মিনিট)। অপেক্ষা করো।
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {seconds} সেকেন্ড হয়েছে...
          </p>
        </>
      ) : (
        <p style={{ fontSize: '1rem' }}>{message}<span className="dots" /></p>
      )}
    </div>
  )
}
