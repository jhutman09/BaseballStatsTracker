export function sortByName<T extends { name: string }>(items: T[] | undefined): T[] {
  return [...(items ?? [])].sort((a, b) => a.name.localeCompare(b.name))
}
