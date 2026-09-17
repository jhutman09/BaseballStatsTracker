import { Link } from 'react-router-dom'

export function Nav() {
  return (
    <nav className="flex gap-4 p-4 border-b border-gray-200">
      <Link to="/" className="text-blue-600 hover:underline">
        Seasons
      </Link>
      <Link to="/clubs" className="text-blue-600 hover:underline">
        Clubs
      </Link>
      <Link to="/players" className="text-blue-600 hover:underline">
        Players
      </Link>
      <Link to="/rosters" className="text-blue-600 hover:underline">
        Rosters
      </Link>
    </nav>
  )
}
