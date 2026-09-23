import { useQuery } from '@tanstack/react-query'
import { apiGet } from '../api/client'
import type { Season } from '../api/types'
import { sortByName } from '../sortByName'

export function SeasonsPage() {
  const { data: seasons, isLoading, error } = useQuery({
    queryKey: ['seasons'],
    queryFn: () => apiGet<Season[]>('/seasons/'),
  })

  if (isLoading) return <p className="p-4">Loading seasons...</p>
  if (error) return <p className="p-4 text-red-600">Failed to load seasons.</p>

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Seasons</h1>
      <ul className="divide-y divide-gray-200">
        {sortByName(seasons).map((season) => (
          <li key={season.id} className="py-2">
            {season.name} ({season.year})
          </li>
        ))}
      </ul>
    </div>
  )
}
