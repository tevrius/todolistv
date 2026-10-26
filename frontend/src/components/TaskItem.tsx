import type { Task } from '../types'
import { useDeleteTask, useUpdateTask } from '../hooks/useTasks'
import { formatDateTime, isOverdue } from '../utils/date'
import { PRIORITY_LABELS, STATUS_LABELS } from '../utils/labels'

interface TaskItemProps {
  task: Task
  onEdit: (task: Task) => void
}

export function TaskItem({ task, onEdit }: TaskItemProps) {
  const update = useUpdateTask()
  const del = useDeleteTask()
  const done = task.status === 'done'

  function toggleDone() {
    update.mutate({ id: task.id, data: { status: done ? 'todo' : 'done' } })
  }

  return (
    <li className={`task-item${done ? ' task-item--done' : ''}`}>
      <input
        type="checkbox"
        className="task-item__check"
        checked={done}
        onChange={toggleDone}
        aria-label="Отметить выполненной"
      />
      <div className="task-item__body">
        <div className="task-item__top">
          <span className="task-item__title">{task.title}</span>
          <span className={`badge badge--priority-${task.priority}`}>
            {PRIORITY_LABELS[task.priority]}
          </span>
          {task.category && <span className="chip">{task.category}</span>}
        </div>
        {task.description && <p className="task-item__description">{task.description}</p>}
        <div className="task-item__meta">
          <span className={`badge badge--status-${task.status}`}>
            {STATUS_LABELS[task.status]}
          </span>
          {task.due_date && (
            <span
              className={`task-item__due${isOverdue(task.due_date, done) ? ' task-item__due--overdue' : ''}`}
            >
              ⏰ Срок: {formatDateTime(task.due_date)}
            </span>
          )}
          <span className="task-item__created">Создана: {formatDateTime(task.created_at)}</span>
        </div>
        {del.isError && (
          <span className="task-item__error">Не удалось удалить: {del.error.message}</span>
        )}
      </div>
      <div className="task-item__actions">
        <button className="btn" onClick={() => onEdit(task)}>
          Изменить
        </button>
        <button
          className="btn btn--ghost-danger"
          onClick={() => del.mutate(task.id)}
          disabled={del.isPending}
        >
          {del.isPending ? 'Удаляю…' : 'Удалить'}
        </button>
      </div>
    </li>
  )
}
