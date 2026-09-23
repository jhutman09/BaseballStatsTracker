import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Club, Roster, RosterEntryWithPlayer, Season } from '../api/types'

interface ParsedPlayer {
  first_name: string
  last_name: string
  jersey_number: number | null
}

// "12 Jake Smith" -> jersey 12; "C. Ellis" -> no jersey. A leading all-digit
// word is the jersey number; the next word is the first name, the rest is the
// last name.
function parseLine(line: string): ParsedPlayer | null {
  const words = line.split(/\s+/)
  let jersey: number | null = null
  if (/^\d+$/.test(words[0])) {
    jersey = Number(words[0])
    words.shift()
  }
  if (words.length < 2) return null
  const [first, ...rest] = words
  return { first_name: first, last_name: rest.join(' '), jersey_number: jersey }
}

export function RosterDetailPage() {
  const { rosterId } = useParams()
  const queryClient = useQueryClient()
  const [bulkText, setBulkText] = useState('')

  const { data: roster, isLoading, error } = useQuery({
    queryKey: ['rosters', rosterId],
    queryFn: () => apiGet<Roster>(`/rosters/${rosterId}`),
  })
  const { data: entries } = useQuery({
    queryKey: ['roster-entries', rosterId],
    queryFn: () => apiGet<RosterEntryWithPlayer[]>(`/rosters/${rosterId}/entries`),
  })
  const { data: seasons } = useQuery({
    queryKey: ['seasons'],
    queryFn: () => apiGet<Season[]>('/seasons/'),
  })
  const { data: clubs } = useQuery({
    queryKey: ['clubs'],
    queryFn: () => apiGet<Club[]>('/clubs/'),
  })

  const lines = bulkText
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
  const parsed = lines.map((line) => ({ line, player: parseLine(line) }))
  const invalidLines = parsed.filter((p) => p.player === null).map((p) => p.line)
  const validPlayers = parsed.flatMap((p) => (p.player ? [p.player] : []))

  const seenNames = new Set(
    (entries ?? []).map((e) => `${e.player.first_name} ${e.player.last_name}`.toLowerCase()),
  )
  const possibleDuplicates: string[] = []
  for (const p of validPlayers) {
    const name = `${p.first_name} ${p.last_name}`
    if (seenNames.has(name.toLowerCase())) possibleDuplicates.push(name)
    seenNames.add(name.toLowerCase())
  }

  const addPlayers = useMutation({
    mutationFn: () => apiPost(`/rosters/${rosterId}/players/bulk`, validPlayers),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roster-entries', rosterId] })
      queryClient.invalidateQueries({ queryKey: ['players'] })
      setBulkText('')
    },
  })

  if (isLoading) return <p className="p-4">Loading roster...</p>
  if (error || !roster) return <p className="p-4 text-red-600">Failed to load roster.</p>

  const clubName = clubs?.find((c) => c.id === roster.club_id)?.name
  const seasonName = seasons?.find((s) => s.id === roster.season_id)?.name

  const sortedEntries = [...(entries ?? [])].sort(
    (a, b) =>
      (a.jersey_number ?? Infinity) - (b.jersey_number ?? Infinity) ||
      a.player.last_name.localeCompare(b.player.last_name) ||
      a.player.first_name.localeCompare(b.player.first_name),
  )

  return (
    <div className="p-4">
      <Link to="/rosters" className="text-blue-600 hover:underline">
        &larr; Rosters
      </Link>
      <h1 className="text-2xl font-bold mt-2">{roster.name}</h1>
      <p className="text-gray-600 mb-4">
        {clubName} &middot; {seasonName}
      </p>

      <div className="mb-4">
        <textarea
          value={bulkText}
          onChange={(e) => setBulkText(e.target.value)}
          placeholder={'One player per line. Optional jersey number first, e.g.\n12 Jake Smith\nC. Ellis'}
          rows={8}
          className="border rounded px-2 py-1 w-full max-w-md"
        />
        {invalidLines.length > 0 && (
          <p className="text-red-600">
            Needs a first and last name: {invalidLines.join('; ')}
          </p>
        )}
        {possibleDuplicates.length > 0 && (
          <p className="text-amber-600">
            Already on this roster or repeated (will still be added):{' '}
            {possibleDuplicates.join('; ')}
          </p>
        )}
        <button
          type="button"
          onClick={() => addPlayers.mutate()}
          disabled={addPlayers.isPending || validPlayers.length === 0 || invalidLines.length > 0}
          className="bg-blue-600 text-white rounded px-3 py-1 mt-2 disabled:opacity-50"
        >
          Add {validPlayers.length} player{validPlayers.length === 1 ? '' : 's'} to roster
        </button>
        {addPlayers.isError && <p className="text-red-600">Failed to add players.</p>}
      </div>

      <h2 className="text-lg font-semibold mb-2">Players ({sortedEntries.length})</h2>
      <ul className="divide-y divide-gray-200">
        {sortedEntries.map((entry) => (
          <li key={entry.id} className="py-2">
            <span className="inline-block w-10 text-gray-500">
              {entry.jersey_number !== null ? `#${entry.jersey_number}` : ''}
            </span>
            {entry.player.first_name} {entry.player.last_name}
          </li>
        ))}
      </ul>
    </div>
  )
}
