import { useEffect, useState, type FormEvent } from 'react'
import type { Task, TaskPriority, TaskStatus } from '../types'
import { useCreateTask, useUpdateTask } from '../hooks/useTasks'
import { fromInputValue, toInputValue } from '../utils/date'
import { PRIORITY_LABELS, STATUS_LABELS } from '../utils/labels'

interface TaskFormModalProps {
  /** null — создание новой задачи, Task — редактирование */
  task: Task | null
  categories: string[]
  onClose: () => void
}

export function TaskFormModal({ task, categories, onClose }: TaskFormModalProps) {
  const create = useCreateTask()
  const update = useUpdateTask()
  const isEdit = task !== null

  const [title, setTitle] = useState(task?.title ?? '')
  const [description, setDescription] = useState(task?.description ?? '')
  const [status, setStatus] = useState<TaskStatus>(task?.status ?? 'todo')
  const [priority, setPriority] = useState<TaskPriority>(task?.priority ?? 'medium')
  const [category, setCategory] = useState(task?.category ?? '')
  const [dueDate, setDueDate] = useState(toInputValue(task?.due_date ?? null))

  const pending = create.isPending || update.isPending
  const error = isEdit ? update.error : create.error

  // Закрытие по Escape
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [onClose])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const data = {
      title: title.trim(),
      description: description.trim() || null,
      status,
      priority,
      category: category.trim() || null,
      due_date: fromInputValue(dueDate),
    }
    try {
      if (isEdit) {
        await update.mutateAsync({ id: task.id, data })
      } else {
        await create.mutateAsync(data)
      }
      onClose()
    } catch {
      // ошибка остаётся в mutation.error и показывается в форме
    }
  }

  return (
    <div
      className="modal-overlay"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <form className="modal" onSubmit={handleSubmit}>
        <h2 className="modal__title">{isEdit ? 'Редактирование задачи' : 'Новая задача'}</h2>

        <label className="field">
          <span className="field__label">Название *</span>
          <input
            required
            autoFocus
            maxLength={200}
            placeholder="Что нужно сделать?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>

        <label className="field">
          <span className="field__label">Описание</span>
          <textarea
            rows={3}
            maxLength={2000}
            placeholder="Подробности (необязательно)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>

        <div className="modal__row">
          <label className="field">
            <span className="field__label">Статус</span>
            <select value={status} onChange={(e) => setStatus(e.target.value as TaskStatus)}>
              {(Object.keys(STATUS_LABELS) as TaskStatus[]).map((s) => (
                <option key={s} value={s}>
                  {STATUS_LABELS[s]}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field__label">Приоритет</span>
            <select value={priority} onChange={(e) => setPriority(e.target.value as TaskPriority)}>
              {(Object.keys(PRIORITY_LABELS) as TaskPriority[]).map((p) => (
                <option key={p} value={p}>
                  {PRIORITY_LABELS[p]}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="modal__row">
          <label className="field">
            <span className="field__label">Категория</span>
            <input
              list="category-options"
              maxLength={64}
              placeholder="например, работа"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            />
            <datalist id="category-options">
              {categories.map((c) => (
                <option key={c} value={c} />
              ))}
            </datalist>
          </label>

          <label className="field">
            <span className="field__label">Срок</span>
            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </label>
        </div>

        {error && <p className="modal__error">Ошибка: {error.message}</p>}

        <div className="modal__actions">
          <button type="button" className="btn" onClick={onClose}>
            Отмена
          </button>
          <button type="submit" className="btn btn--primary" disabled={pending || !title.trim()}>
            {pending ? 'Сохраняю…' : isEdit ? 'Сохранить' : 'Создать'}
          </button>
        </div>
      </form>
    </div>
  )
}
