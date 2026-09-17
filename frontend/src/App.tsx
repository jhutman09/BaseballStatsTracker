import { Routes, Route } from 'react-router-dom'
import { SeasonsPage } from './pages/SeasonsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<SeasonsPage />} />
    </Routes>
  )
}

export default App
