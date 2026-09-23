import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Player } from '../api/types'

export function PlayersPage() {
  const queryClient = useQueryClient()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const firstNameRef = useRef<HTMLInputElement>(null)

  const { data: players, isLoading, error } = useQuery({
    queryKey: ['players'],
    queryFn: () => apiGet<Player[]>('/players/'),
  })

  const createPlayer = useMutation({
    mutationFn: () =>
      apiPost<Player>('/players/', { first_name: firstName, last_name: lastName }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['players'] })
      setFirstName('')
      setLastName('')
      firstNameRef.current?.focus()
    },
  })

  const [bulkText, setBulkText] = useState('')

  const bulkLines = bulkText
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
  const invalidLines = bulkLines.filter((line) => line.split(/\s+/).length < 2)
  const parsedBulk = bulkLines
    .filter((line) => !invalidLines.includes(line))
    .map((line) => {
      const [first, ...rest] = line.split(/\s+/)
      return { first_name: first, last_name: rest.join(' ') }
    })
  const seenNames = new Set(
    (players ?? []).map((p) => `${p.first_name} ${p.last_name}`.toLowerCase()),
  )
  const possibleDuplicates: string[] = []
  for (const p of parsedBulk) {
    const key = `${p.first_name} ${p.last_name}`.toLowerCase()
    if (seenNames.has(key)) possibleDuplicates.push(`${p.first_name} ${p.last_name}`)
    seenNames.add(key)
  }

  const createPlayersBulk = useMutation({
    mutationFn: () => apiPost<Player[]>('/players/bulk', parsedBulk),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['players'] })
      setBulkText('')
    },
  })

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Players</h1>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          createPlayer.mutate()
        }}
        className="flex gap-2 mb-4"
      >
        <input
          ref={firstNameRef}
          autoFocus
          type="text"
          placeholder="First name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <input
          type="text"
          placeholder="Last name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <button
          type="submit"
          disabled={createPlayer.isPending}
          className="bg-blue-600 text-white rounded px-3 py-1 disabled:opacity-50"
        >
          Add Player
        </button>
      </form>
      {createPlayer.isError && (
        <p className="text-red-600 mb-4">Failed to add player.</p>
      )}

      <details className="mb-4">
        <summary className="cursor-pointer text-blue-600">Bulk add</summary>
        <div className="mt-2">
          <textarea
            value={bulkText}
            onChange={(e) => setBulkText(e.target.value)}
            placeholder={'One player per line, e.g.\nJake Smith\nMaria Garcia'}
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
              Already exists or repeated (will still be added): {possibleDuplicates.join('; ')}
            </p>
          )}
          <button
            type="button"
            onClick={() => createPlayersBulk.mutate()}
            disabled={
              createPlayersBulk.isPending ||
              parsedBulk.length === 0 ||
              invalidLines.length > 0
            }
            className="bg-blue-600 text-white rounded px-3 py-1 mt-2 disabled:opacity-50"
          >
            Add {parsedBulk.length} player{parsedBulk.length === 1 ? '' : 's'}
          </button>
          {createPlayersBulk.isError && (
            <p className="text-red-600">Failed to add players.</p>
          )}
        </div>
      </details>

      {isLoading && <p>Loading players...</p>}
      {error && <p className="text-red-600">Failed to load players.</p>}
      <ul className="divide-y divide-gray-200">
        {[...(players ?? [])]
          .sort(
            (a, b) =>
              a.last_name.localeCompare(b.last_name) ||
              a.first_name.localeCompare(b.first_name),
          )
          .map((player) => (
          <li key={player.id} className="py-2">
            {player.first_name} {player.last_name}
          </li>
        ))}
      </ul>
    </div>
  )
}
