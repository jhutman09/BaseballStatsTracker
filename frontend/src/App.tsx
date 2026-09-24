import { Routes, Route } from 'react-router-dom'
import { Nav } from './components/Nav'
import { SeasonsPage } from './pages/SeasonsPage'
import { ClubsPage } from './pages/ClubsPage'
import { PlayersPage } from './pages/PlayersPage'
import { RostersPage } from './pages/RostersPage'
import { RosterDetailPage } from './pages/RosterDetailPage'
import { GamesPage } from './pages/GamesPage'
import { GameDetailPage } from './pages/GameDetailPage'

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<SeasonsPage />} />
        <Route path="/clubs" element={<ClubsPage />} />
        <Route path="/players" element={<PlayersPage />} />
        <Route path="/rosters" element={<RostersPage />} />
        <Route path="/rosters/:rosterId" element={<RosterDetailPage />} />
        <Route path="/games" element={<GamesPage />} />
        <Route path="/games/:gameId" element={<GameDetailPage />} />
      </Routes>
    </>
  )
}

export default App
