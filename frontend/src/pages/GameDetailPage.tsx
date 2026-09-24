import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { apiGet } from '../api/client'
import type { Club, Game, LineupEntry, Roster } from '../api/types'
import { LineupEditor } from '../components/LineupEditor'

export function GameDetailPage() {
  const { gameId } = useParams()

  const { data: game, isLoading, error } = useQuery({
    queryKey: ['games', gameId],
    queryFn: () => apiGet<Game>(`/games/${gameId}`),
  })
  const { data: lineups } = useQuery({
    queryKey: ['lineups', gameId],
    queryFn: () => apiGet<LineupEntry[]>(`/games/${gameId}/lineups`),
  })
  const { data: rosters } = useQuery({
    queryKey: ['rosters'],
    queryFn: () => apiGet<Roster[]>('/rosters/'),
  })
  const { data: clubs } = useQuery({
    queryKey: ['clubs'],
    queryFn: () => apiGet<Club[]>('/clubs/'),
  })

  if (isLoading || !lineups || !rosters || !clubs) return <p className="p-4">Loading game...</p>
  if (error || !game) return <p className="p-4 text-red-600">Failed to load game.</p>

  function teamName(rosterId: number) {
    const roster = rosters!.find((r) => r.id === rosterId)
    return clubs!.find((c) => c.id === roster?.club_id)?.name ?? `Roster ${rosterId}`
  }

  const away = teamName(game.away_roster_id)
  const home = teamName(game.home_roster_id)

  return (
    <div className="p-4">
      <Link to="/games" className="text-blue-600 hover:underline">
        &larr; Games
      </Link>
      <h1 className="text-2xl font-bold mt-2">
        {away} at {home}
      </h1>
      <p className="text-gray-600 mb-6">
        {game.game_date}
        {game.field ? ` · ${game.field}` : ''}
        {game.away_score !== null && game.home_score !== null
          ? ` · ${away} ${game.away_score}, ${home} ${game.home_score}`
          : ''}
      </p>

      <LineupEditor
        key={`away-${game.away_roster_id}`}
        gameId={game.id}
        rosterId={game.away_roster_id}
        title={`${away} (visiting, top)`}
        initialEntries={lineups.filter((e) => e.roster_id === game.away_roster_id)}
      />
      <LineupEditor
        key={`home-${game.home_roster_id}`}
        gameId={game.id}
        rosterId={game.home_roster_id}
        title={`${home} (home, bottom)`}
        initialEntries={lineups.filter((e) => e.roster_id === game.home_roster_id)}
      />
    </div>
  )
}
