import { Routes, Route } from 'react-router-dom'
import { Nav } from './components/Nav'
import { SeasonsPage } from './pages/SeasonsPage'
import { ClubsPage } from './pages/ClubsPage'

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<SeasonsPage />} />
        <Route path="/clubs" element={<ClubsPage />} />
      </Routes>
    </>
  )
}

export default App
