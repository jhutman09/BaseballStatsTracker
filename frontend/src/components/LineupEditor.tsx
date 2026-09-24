import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiGet, apiPost, apiPut } from '../api/client'
import type { LineupEntry, RosterEntryWithPlayer } from '../api/types'

interface Stint {
  key: number
  slot: number
  playerId: string
  position: string
  inning: string
}

interface Props {
  gameId: number
  rosterId: number
  title: string
  initialEntries: LineupEntry[]
}

const DEFAULT_SLOTS = 9

export function LineupEditor({ gameId, rosterId, title, initialEntries }: Props) {
  const queryClient = useQueryClient()
  const nextKey = useRef(0)
  const newKey = () => nextKey.current++

  const [stints, setStints] = useState<Stint[]>(() => {
    if (initialEntries.length > 0) {
      return initialEntries.map((e) => ({
        key: newKey(),
        slot: e.batting_slot,
        playerId: String(e.player_id),
        position: e.position,
        inning: e.inning_entered === null ? '' : String(e.inning_entered),
      }))
    }
    return Array.from({ length: DEFAULT_SLOTS }, (_, i) => ({
      key: newKey(),
      slot: i + 1,
      playerId: '',
      position: '',
      inning: '',
    }))
  })
  const [newFirst, setNewFirst] = useState('')
  const [newLast, setNewLast] = useState('')
  const [validationError, setValidationError] = useState('')

  const { data: rosterEntries } = useQuery({
    queryKey: ['roster-entries', String(rosterId)],
    queryFn: () => apiGet<RosterEntryWithPlayer[]>(`/rosters/${rosterId}/entries`),
  })

  const players = [...(rosterEntries ?? [])]
    .map((e) => e.player)
    .sort(
      (a, b) => a.last_name.localeCompare(b.last_name) || a.first_name.localeCompare(b.first_name),
    )

  const save = useMutation({
    mutationFn: () => {
      const body = stints
        .filter((s) => s.playerId !== '')
        .map((s) => ({
          player_id: Number(s.playerId),
          batting_slot: s.slot,
          position: s.position.trim(),
          inning_entered: s.inning.trim() === '' ? null : Number(s.inning),
        }))
      return apiPut<LineupEntry[]>(`/games/${gameId}/lineups/${rosterId}`, body)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lineups', String(gameId)] })
    },
  })

  const addPlayer = useMutation({
    mutationFn: () =>
      apiPost(`/rosters/${rosterId}/players/bulk`, [
        { first_name: newFirst.trim(), last_name: newLast.trim() },
      ]),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roster-entries', String(rosterId)] })
      queryClient.invalidateQueries({ queryKey: ['players'] })
      setNewFirst('')
      setNewLast('')
    },
  })

  function update(key: number, patch: Partial<Stint>) {
    setStints((prev) => prev.map((s) => (s.key === key ? { ...s, ...patch } : s)))
  }

  function addSubstitute(after: Stint) {
    setStints((prev) => {
      const index = prev.findIndex((s) => s.key === after.key)
      const next: Stint = { key: newKey(), slot: after.slot, playerId: '', position: '', inning: '' }
      return [...prev.slice(0, index + 1), next, ...prev.slice(index + 1)]
    })
  }

  function addSlot() {
    const nextSlot = Math.max(0, ...stints.map((s) => s.slot)) + 1
    setStints((prev) => [
      ...prev,
      { key: newKey(), slot: nextSlot, playerId: '', position: '', inning: '' },
    ])
  }

  function handleSave() {
    setValidationError('')
    const filled = stints.filter((s) => s.playerId !== '')
    if (filled.some((s) => s.position.trim() === '')) {
      setValidationError('Every player in the lineup needs a position.')
      return
    }
    if (filled.some((s) => s.inning.trim() !== '' && !/^\d+$/.test(s.inning.trim()))) {
      setValidationError('Inning must be a whole number.')
      return
    }
    save.mutate()
  }

  const slotStintCount = (slot: number) => stints.filter((s) => s.slot === slot).length

  return (
    <section className="mb-8">
      <h2 className="text-lg font-semibold mb-2">{title}</h2>
      <table className="border-collapse">
        <thead>
          <tr className="text-left text-sm text-gray-600">
            <th className="pr-2">Slot</th>
            <th className="pr-2">Player</th>
            <th className="pr-2">Pos</th>
            <th className="pr-2">Inn in</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {stints.map((s) => {
            const isFirstOfSlot = stints.find((x) => x.slot === s.slot)?.key === s.key
            return (
              <tr key={s.key}>
                <td className="pr-2 py-1 w-10">{isFirstOfSlot ? s.slot : ''}</td>
                <td className="pr-2 py-1">
                  <select
                    value={s.playerId}
                    onChange={(e) => update(s.key, { playerId: e.target.value })}
                    className="border rounded px-2 py-1"
                  >
                    <option value="">—</option>
                    {players.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.last_name}, {p.first_name}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="pr-2 py-1">
                  <input
                    type="text"
                    value={s.position}
                    onChange={(e) => update(s.key, { position: e.target.value })}
                    placeholder="6 or SS"
                    className="border rounded px-2 py-1 w-20"
                  />
                </td>
                <td className="pr-2 py-1">
                  <input
                    type="number"
                    min={1}
                    step={1}
                    value={s.inning}
                    onChange={(e) => update(s.key, { inning: e.target.value })}
                    placeholder="start"
                    className="border rounded px-2 py-1 w-20"
                  />
                </td>
                <td className="py-1 whitespace-nowrap">
                  <button
                    type="button"
                    onClick={() => addSubstitute(s)}
                    className="text-blue-600 hover:underline mr-2"
                  >
                    + sub / move
                  </button>
                  {slotStintCount(s.slot) > 1 && (
                    <button
                      type="button"
                      onClick={() => setStints((prev) => prev.filter((x) => x.key !== s.key))}
                      className="text-red-600 hover:underline"
                    >
                      remove
                    </button>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>

      <button type="button" onClick={addSlot} className="text-blue-600 hover:underline mt-1">
        + add batting slot
      </button>

      <div className="mt-3 flex flex-wrap gap-2 items-center">
        <button
          type="button"
          onClick={handleSave}
          disabled={save.isPending}
          className="bg-blue-600 text-white rounded px-3 py-1 disabled:opacity-50"
        >
          Save lineup
        </button>
        {save.isSuccess && <span className="text-green-700">Saved.</span>}
        {validationError && <span className="text-red-600">{validationError}</span>}
        {save.isError && <span className="text-red-600">{save.error.message}</span>}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          addPlayer.mutate()
        }}
        className="mt-4 flex flex-wrap gap-2 items-center text-sm"
      >
        <span className="text-gray-600">Not on the roster yet?</span>
        <input
          type="text"
          placeholder="First name"
          value={newFirst}
          onChange={(e) => setNewFirst(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <input
          type="text"
          placeholder="Last name"
          value={newLast}
          onChange={(e) => setNewLast(e.target.value)}
          className="border rounded px-2 py-1"
          required
        />
        <button
          type="submit"
          disabled={addPlayer.isPending}
          className="border rounded px-3 py-1 disabled:opacity-50"
        >
          Add to roster
        </button>
        {addPlayer.isError && <span className="text-red-600">Failed to add player.</span>}
      </form>
    </section>
  )
}
