const API_BASE_URL = 'http://127.0.0.1:8000'

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    throw new Error(`GET ${path} failed: ${response.status}`)
  }
  return response.json()
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw new Error(`POST ${path} failed: ${response.status}`)
  }
  return response.json()
}

export async function apiPatch<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw new Error(`PATCH ${path} failed: ${response.status}`)
  }
  return response.json()
}

export async function apiPut<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    let detail = ''
    try {
      const data = await response.json()
      if (typeof data.detail === 'string') detail = `: ${data.detail}`
    } catch {
      // response had no JSON body
    }
    throw new Error(`PUT ${path} failed (${response.status})${detail}`)
  }
  return response.json()
}
