import { useAuthStore } from './stores/auth'

export const AUTH_API = 'http://158.160.231.42:8002'
export const TASK_API = 'http://158.160.231.42:8003'

async function parseError(response) {
  let data = {}
  try {
    data = await response.json()
  } catch {
    data = {}
  }
  if (response.status === 401) {
    useAuthStore().logout()
    window.location.assign('/')
    return 'Сессия истекла, войдите снова'
  }
  if (data && typeof data === 'object') {
    const firstKey = Object.keys(data)[0]
    if (firstKey) {
      const value = data[firstKey]
      if (Array.isArray(value) && value.length) return value[0]
      if (firstKey === 'detail') return data.detail
      return `Ошибка: ${value}`
    }
  }
  return 'Ошибка запроса'
}

export async function apiFetch(base, path, options = {}) {
  const auth = useAuthStore()
  const headers = { Authorization: `Bearer ${auth.token}` }
  if (options.body && typeof options.body !== 'string') {
    headers['Content-Type'] = 'application/json'
    options.body = JSON.stringify(options.body)
  } else if (options.body) {
    headers['Content-Type'] = 'application/json'
  }

  const response = await fetch(`${base}${path}`, { ...options, headers })

  if (!response.ok) {
    const message = await parseError(response)
    throw new Error(message)
  }
  if (response.status === 204) return null
  return response.json()
}
