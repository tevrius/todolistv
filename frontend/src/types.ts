export type TaskStatus = 'todo' | 'in_progress' | 'done'
export type TaskPriority = 'low' | 'medium' | 'high'
export type SortField = 'created_at' | 'updated_at' | 'due_date' | 'priority' | 'title'
export type SortOrder = 'asc' | 'desc'

/** Задача в ответах API */
export interface Task {
  id: string
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  category: string | null
  due_date: string | null
  created_at: string
  updated_at: string
}

/** Данные для создания/редактирования задачи */
export interface TaskInput {
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  category: string | null
  due_date: string | null
}

/** Страница списка задач */
export interface TaskPage {
  items: Task[]
  total: number
  limit: number
  offset: number
}

/** Параметры запроса списка */
export interface TaskFilters {
  status?: TaskStatus
  priority?: TaskPriority
  category?: string
  search?: string
  sort_by: SortField
  sort_order: SortOrder
  limit: number
  offset: number
}

/** Состояние панели фильтров в UI */
export interface FiltersState {
  status: TaskStatus | ''
  priority: TaskPriority | ''
  category: string
  search: string
  sortBy: SortField
  sortOrder: SortOrder
  limit: number
}
