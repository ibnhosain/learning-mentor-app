import { Link, useNavigate } from 'react-router-dom'
import { clearTokens } from '../api/client'

export default function Navbar() {
  const navigate = useNavigate()

  function logout() {
    clearTokens()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-title">📚 Learning Mentor</Link>
      <div className="navbar-links">
        <Link to="/progress" className="navbar-link">অগ্রগতি</Link>
        <button onClick={logout} className="navbar-link">বের হও</button>
      </div>
    </nav>
  )
}
