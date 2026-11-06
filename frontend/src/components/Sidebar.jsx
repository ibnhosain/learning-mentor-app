import { NavLink, useNavigate } from 'react-router-dom'
import { clearTokens } from '../api/client'
import { useApp } from '../context/AppContext'

const NAV = [
  { to: '/',             icon: '🏠', label: 'আজকের পাঠ' },
  { to: 'SUBMIT',        icon: '✍️', label: 'কাজ জমা দাও' },
  { to: '/my-learning',  icon: '📚', label: 'আমার শেখা' },
  { to: '/modules',      icon: '📋', label: 'মডিউল সমূহ' },
  { to: '/progress',     icon: '📊', label: 'আমার অগ্রগতি' },
]

export default function Sidebar() {
  const navigate = useNavigate()
  const { currentLessonId } = useApp()

  function handleNav(item, e) {
    if (item.to === 'SUBMIT') {
      e.preventDefault()
      if (currentLessonId) navigate(`/submit/${currentLessonId}`)
      else navigate('/')
    }
  }

  function logout() {
    clearTokens()
    navigate('/login')
  }

  return (
    <>
      {/* ── Desktop sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span style={{ fontSize: '1.5rem' }}>📖</span>
          <span className="sidebar-logo-text">Learning Mentor</span>
        </div>

        <nav className="sidebar-nav">
          {NAV.map(item => (
            <NavLink
              key={item.label}
              to={item.to === 'SUBMIT' ? '#' : item.to}
              onClick={item.to === 'SUBMIT' ? e => handleNav(item, e) : undefined}
              end={item.to === '/'}
              className={({ isActive }) =>
                'sidebar-link' + (isActive && item.to !== 'SUBMIT' ? ' active' : '')
              }
            >
              <span className="sidebar-icon">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <button className="sidebar-link sidebar-logout" onClick={logout}>
          <span className="sidebar-icon">🚪</span>
          <span>বের হও</span>
        </button>
      </aside>

      {/* ── Mobile bottom nav ── */}
      <nav className="bottom-nav">
        {NAV.map(item => (
          <NavLink
            key={item.label}
            to={item.to === 'SUBMIT' ? '#' : item.to}
            onClick={item.to === 'SUBMIT' ? e => handleNav(item, e) : undefined}
            end={item.to === '/'}
            className={({ isActive }) =>
              'bottom-nav-item' + (isActive && item.to !== 'SUBMIT' ? ' active' : '')
            }
          >
            <span style={{ fontSize: '1.3rem' }}>{item.icon}</span>
            <span className="bottom-nav-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </>
  )
}
