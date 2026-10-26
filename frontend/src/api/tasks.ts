import { request } from './client'
import type { Task, TaskFilters, TaskInput, TaskPage } from '../types'

const BASE = '/api/v1'

function buildQuery(filters: TaskFilters): string {
  const params = new URLSearchParams()
  if (filters.status) params.set('status', filters.status)
  if (filters.priority) params.set('priority', filters.priority)
  if (filters.category) params.set('category', filters.category)
  if (filters.search) params.set('search', filters.search)
  params.set('sort_by', filters.sort_by)
  params.set('sort_order', filters.sort_order)
  params.set('limit', String(filters.limit))
  params.set('offset', String(filters.offset))
  const qs = params.toString()
  return qs ? `?${qs}` : ''
}

export function fetchTasks(filters: TaskFilters): Promise<TaskPage> {
  return request<TaskPage>(`${BASE}/tasks${buildQuery(filters)}`)
}

export function fetchCategories(): Promise<string[]> {
  return request<string[]>(`${BASE}/tasks/categories`)
}

export function createTask(data: TaskInput): Promise<Task> {
  return request<Task>(`${BASE}/tasks`, { method: 'POST', body: JSON.stringify(data) })
}

export function updateTask(id: string, data: Partial<TaskInput>): Promise<Task> {
  return request<Task>(`${BASE}/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export function deleteTask(id: string): Promise<void> {
  return request<void>(`${BASE}/tasks/${id}`, { method: 'DELETE' })
}
