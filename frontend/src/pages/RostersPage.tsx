import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Roster, Season, Club } from '../api/types'

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

  function seasonName(seasonId: number) {
    return seasons?.find((s) => s.id === seasonId)?.name ?? seasonId
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
          {seasons?.map((season) => (
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
          {clubs?.map((club) => (
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
      <ul className="divide-y divide-gray-200">
        {rosters?.map((roster) => (
          <li key={roster.id} className="py-2">
            {roster.name} — {clubName(roster.club_id)} ({seasonName(roster.season_id)})
          </li>
        ))}
      </ul>
    </div>
  )
}
