import { useQuery } from '@tanstack/react-query'
import { apiGet } from '../api/client'
import type { Club } from '../api/types'
import { sortByName } from '../sortByName'

export function ClubsPage() {
  const { data: clubs, isLoading, error } = useQuery({
    queryKey: ['clubs'],
    queryFn: () => apiGet<Club[]>('/clubs/'),
  })

  if (isLoading) return <p className="p-4">Loading clubs...</p>
  if (error) return <p className="p-4 text-red-600">Failed to load clubs.</p>

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Clubs</h1>
      <ul className="divide-y divide-gray-200">
        {sortByName(clubs).map((club) => (
          <li key={club.id} className="py-2">
            {club.name}
          </li>
        ))}
      </ul>
    </div>
  )
}
