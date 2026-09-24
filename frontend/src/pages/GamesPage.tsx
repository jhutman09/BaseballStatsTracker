import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Club, Game, Roster, Season } from '../api/types'
import { sortByName } from '../sortByName'

export function GamesPage() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const [seasonId, setSeasonId] = useState('')
  const [awayId, setAwayId] = useState('')
  const [homeId, setHomeId] = useState('')
  const [gameDate, setGameDate] = useState('')
  const [field, setField] = useState('')
  const [awayScore, setAwayScore] = useState('')
  const [homeScore, setHomeScore] = useState('')
  const [formError, setFormError] = useState('')

  const { data: games, isLoading, error } = useQuery({
    queryKey: ['games'],
    queryFn: () => apiGet<Game[]>('/games/'),
  })
  const { data: rosters } = useQuery({
    queryKey: ['rosters'],
    queryFn: () => apiGet<Roster[]>('/rosters/'),
  })
  const { data: clubs } = useQuery({
    queryKey: ['clubs'],
    queryFn: () => apiGet<Club[]>('/clubs/'),
  })
  const { data: allEntries } = useQuery({
    queryKey: ['roster-entries-all'],
    queryFn: () => apiGet<{ roster_id: number }[]>('/roster-entries/'),
  })
  const { data: seasons } = useQuery({
    queryKey: ['seasons'],
    queryFn: () => apiGet<Season[]>('/seasons/'),
  })

  function teamName(rosterId: number) {
    const roster = rosters?.find((r) => r.id === rosterId)
    return clubs?.find((c) => c.id === roster?.club_id)?.name ?? `Roster ${rosterId}`
  }

  const rosterIdsWithPlayers = new Set((allEntries ?? []).map((e) => e.roster_id))
  const seasonRosters = (rosters ?? [])
    .filter((r) => String(r.season_id) === seasonId && rosterIdsWithPlayers.has(r.id))
    .map((r) => ({ id: r.id, name: teamName(r.id) }))
  const rosterOptions = sortByName(seasonRosters)

  const createGame = useMutation({
    mutationFn: () =>
      apiPost<Game>('/games/', {
        home_roster_id: Number(homeId),
        away_roster_id: Number(awayId),
        game_date: gameDate,
        field: field.trim() === '' ? null : field.trim(),
        away_score: awayScore === '' ? null : Number(awayScore),
        home_score: homeScore === '' ? null : Number(homeScore),
      }),
    onSuccess: (game) => {
      queryClient.invalidateQueries({ queryKey: ['games'] })
      navigate(`/games/${game.id}`)
    },
  })

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setFormError('')
    if (homeId === awayId) {
      setFormError('Home and away must be different teams.')
      return
    }
    createGame.mutate()
  }

  const sortedGames = [...(games ?? [])].sort(
    (a, b) => b.game_date.localeCompare(a.game_date) || b.id - a.id,
  )

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Games</h1>

      <form onSubmit={handleSubmit} className="flex flex-wrap gap-2 items-center mb-4">
        <select
          value={seasonId}
          onChange={(e) => {
            setSeasonId(e.target.value)
            setAwayId('')
            setHomeId('')
          }}
          className="border rounded px-2 py-1"
          required
        >
          <option value="" disabled>
            Season
          </option>
          {sortByName(seasons).map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
        <select
          value={awayId}
          onChange={(e) => setAwayId(e.target.value)}
          disabled={seasonId === ''}
          className="border rounded px-2 py-1 disabled:opacity-50"
          required
        >
          <option value="" disabled>
            {seasonId === '' ? 'Pick a season first' : rosterOptions.length === 0 ? 'No teams with players' : 'Visiting team'}
          </option>
          {rosterOptions.filter((r) => String(r.id) !== homeId).map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
        <select
          value={homeId}
          onChange={(e) => setHomeId(e.target.value)}
          disabled={seasonId === ''}
          className="border rounded px-2 py-1 disabled:opacity-50"
          required
        >
          <option value="" disabled>
            {seasonId === '' ? 'Pick a season first' : rosterOptions.length === 0 ? 'No teams with players' : 'Home team'}
          </option>
          {rosterOptions.filter((r) => String(r.id) !== awayId).map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
        <input
          type="date"
          value={gameDate}
          onChange={(e) => setGameDate(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <input
          type="text"
          placeholder="Field"
          value={field}
          onChange={(e) => setField(e.target.value)}
          className="border rounded px-2 py-1 w-24"
        />
        <input
          type="number"
          min={0}
          placeholder="Away score"
          value={awayScore}
          onChange={(e) => setAwayScore(e.target.value)}
          className="border rounded px-2 py-1 w-28"
        />
        <input
          type="number"
          min={0}
          placeholder="Home score"
          value={homeScore}
          onChange={(e) => setHomeScore(e.target.value)}
          className="border rounded px-2 py-1 w-28"
        />
        <button
          type="submit"
          disabled={createGame.isPending}
          className="bg-blue-600 text-white rounded px-3 py-1 disabled:opacity-50"
        >
          Create game
        </button>
      </form>
      {formError && <p className="text-red-600 mb-4">{formError}</p>}
      {createGame.isError && <p className="text-red-600 mb-4">Failed to create game.</p>}

      {isLoading && <p>Loading games...</p>}
      {error && <p className="text-red-600">Failed to load games.</p>}
      <ul className="divide-y divide-gray-200">
        {sortedGames.map((game) => (
          <li key={game.id} className="py-2">
            <Link to={`/games/${game.id}`} className="text-blue-600 hover:underline">
              {teamName(game.away_roster_id)} at {teamName(game.home_roster_id)}
            </Link>{' '}
            <span className="text-gray-600">
              — {game.game_date}
              {game.away_score !== null && game.home_score !== null
                ? ` (${game.away_score}-${game.home_score})`
                : ''}
            </span>
          </li>
        ))}
        {sortedGames.length === 0 && !isLoading && (
          <li className="py-2 text-gray-500">No games yet.</li>
        )}
      </ul>
    </div>
  )
}
