import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost } from '../api/client'
import type { Player } from '../api/types'

export function PlayersPage() {
  const queryClient = useQueryClient()
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')

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

      {isLoading && <p>Loading players...</p>}
      {error && <p className="text-red-600">Failed to load players.</p>}
      <ul className="divide-y divide-gray-200">
        {players?.map((player) => (
          <li key={player.id} className="py-2">
            {player.first_name} {player.last_name}
          </li>
        ))}
      </ul>
    </div>
  )
}
