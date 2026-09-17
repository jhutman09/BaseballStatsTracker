export interface Season {
  id: number
  name: string
  year: number
  start_date: string | null
  end_date: string | null
}

export interface Club {
  id: number
  name: string
}

export interface Player {
  id: number
  first_name: string
  last_name: string
  notes: string | null
}

export interface Roster {
  id: number
  season_id: number
  club_id: number
  name: string
}
