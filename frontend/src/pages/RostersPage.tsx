import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Roster, Season, Club } from '../api/types'
import { sortByName } from '../sortByName'

export function RostersPage() {
  const queryClient = useQueryClient()
  const [seasonId, setSeasonId] = useState('')
  const [clubId, setClubId] = useState('')
  const [name, setName] = useState('')

  const { data: rosters, isLoading, error } = useQuery({
    queryKey: ['rosters'],
    queryFn: () => apiGet<Roster[]>('/rosters/'),
  })

  const { data: seasons } = useQuery({
    queryKey: ['seasons'],
    queryFn: () => apiGet<Season[]>('/seasons/'),
  })

  const { data: clubs } = useQuery({
    queryKey: ['clubs'],
    queryFn: () => apiGet<Club[]>('/clubs/'),
  })

  const createRoster = useMutation({
    mutationFn: () =>
      apiPost<Roster>('/rosters/', {
        season_id: Number(seasonId),
        club_id: Number(clubId),
        name,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['rosters'] })
      setName('')
    },
  })

  function clubName(clubId: number) {
    return clubs?.find((c) => c.id === clubId)?.name ?? clubId
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Rosters</h1>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          createRoster.mutate()
        }}
        className="flex gap-2 mb-4"
      >
        <select
          value={seasonId}
          onChange={(e) => setSeasonId(e.target.value)}
          className="border rounded px-2 py-1"
          required
        >
          <option value="" disabled>
            Season
          </option>
          {sortByName(seasons).map((season) => (
            <option key={season.id} value={season.id}>
              {season.name}
            </option>
          ))}
        </select>
        <select
          value={clubId}
          onChange={(e) => setClubId(e.target.value)}
          className="border rounded px-2 py-1"
          required
        >
          <option value="" disabled>
            Club
          </option>
          {sortByName(clubs).map((club) => (
            <option key={club.id} value={club.id}>
              {club.name}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Roster name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <button
          type="submit"
          disabled={createRoster.isPending}
          className="bg-blue-600 text-white rounded px-3 py-1 disabled:opacity-50"
        >
          Add Roster
        </button>
      </form>
      {createRoster.isError && (
        <p className="text-red-600 mb-4">Failed to add roster.</p>
      )}

      {isLoading && <p>Loading rosters...</p>}
      {error && <p className="text-red-600">Failed to load rosters.</p>}
      <div className="space-y-2">
        {[...(seasons ?? [])]
          .sort((a, b) => a.year - b.year)
          .map((season) => {
            const seasonRosters = (rosters ?? [])
              .filter((r) => r.season_id === season.id)
              .sort((a, b) => String(clubName(a.club_id)).localeCompare(String(clubName(b.club_id))))
            return (
              <details key={season.id} className="border rounded">
                <summary className="cursor-pointer px-4 py-3 font-semibold flex justify-between">
                  <span>{season.name}</span>
                  <span className="text-gray-500 font-normal">
                    {seasonRosters.length} roster{seasonRosters.length === 1 ? '' : 's'}
                  </span>
                </summary>
                <ul className="divide-y divide-gray-200 border-t">
                  {seasonRosters.map((roster) => (
                    <li key={roster.id} className="px-4 py-2">
                      <Link to={`/rosters/${roster.id}`} className="text-blue-600 hover:underline">
                        {roster.name}
                      </Link>{' '}
                      — {clubName(roster.club_id)}
                    </li>
                  ))}
                  {seasonRosters.length === 0 && (
                    <li className="px-4 py-2 text-gray-500">No rosters yet.</li>
                  )}
                </ul>
              </details>
            )
          })}
      </div>
    </div>
  )
}
