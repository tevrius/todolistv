import type { SortField, TaskPriority, TaskStatus } from '../types'

export const STATUS_LABELS: Record<TaskStatus, string> = {
  todo: 'К выполнению',
  in_progress: 'В работе',
  done: 'Готово',
}

export const PRIORITY_LABELS: Record<TaskPriority, string> = {
  low: 'Низкий',
  medium: 'Средний',
  high: 'Высокий',
}

export const SORT_FIELD_LABELS: Record<SortField, string> = {
  created_at: 'Дата создания',
  updated_at: 'Дата изменения',
  due_date: 'Срок',
  priority: 'Приоритет',
  title: 'Название',
}

export const SORT_ORDER_LABELS = {
  asc: 'По возрастанию',
  desc: 'По убыванию',
} as const
