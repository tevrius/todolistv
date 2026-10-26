import { useMemo, useState } from 'react'
import { FiltersBar } from './components/FiltersBar'
import { Pagination } from './components/Pagination'
import { TaskFormModal } from './components/TaskFormModal'
import { TaskList } from './components/TaskList'
import { useDebounced } from './hooks/useDebounced'
import { useCategories, useTasks } from './hooks/useTasks'
import type { FiltersState, Task } from './types'

const DEFAULT_FILTERS: FiltersState = {
  status: '',
  priority: '',
  category: '',
  search: '',
  sortBy: 'created_at',
  sortOrder: 'desc',
  limit: 20,
}

type ModalState = { type: 'new' } | { type: 'edit'; task: Task } | null

export default function App() {
  const [filters, setFilters] = useState<FiltersState>(DEFAULT_FILTERS)
  const [page, setPage] = useState(1)
  const [modal, setModal] = useState<ModalState>(null)
  const debouncedSearch = useDebounced(filters.search)

  const categories = useCategories()
  const categoryList = categories.data ?? []

  const queryFilters = useMemo(
    () => ({
      status: filters.status || undefined,
      priority: filters.priority || undefined,
      category: filters.category || undefined,
      search: debouncedSearch.trim() || undefined,
      sort_by: filters.sortBy,
      sort_order: filters.sortOrder,
      limit: filters.limit,
      offset: (page - 1) * filters.limit,
    }),
    [filters, page, debouncedSearch],
  )

  const tasks = useTasks(queryFilters)

  function changeFilters(partial: Partial<FiltersState>) {
    setFilters((prev) => ({ ...prev, ...partial }))
    setPage(1)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-header__title">TodoList</h1>
        <button className="btn btn--primary" onClick={() => setModal({ type: 'new' })}>
          + Новая задача
        </button>
      </header>

      <FiltersBar
        filters={filters}
        categories={categoryList}
        onChange={changeFilters}
        onReset={() => changeFilters(DEFAULT_FILTERS)}
      />

      {tasks.isPending && <div className="loading">Загрузка…</div>}

      {tasks.isError && (
        <div className="error-banner">
          <span>Не удалось загрузить задачи: {tasks.error.message}</span>
          <button className="btn" onClick={() => tasks.refetch()}>
            Повторить
          </button>
        </div>
      )}

      {tasks.data && (
        <>
          <TaskList
            tasks={tasks.data.items}
            onEdit={(task) => setModal({ type: 'edit', task })}
          />
          <Pagination
            total={tasks.data.total}
            limit={filters.limit}
            offset={queryFilters.offset}
            onPageChange={setPage}
            onLimitChange={(limit) => changeFilters({ limit })}
          />
        </>
      )}

      {modal && (
        <TaskFormModal
          key={modal.type === 'edit' ? modal.task.id : 'new'}
          task={modal.type === 'edit' ? modal.task : null}
          categories={categoryList}
          onClose={() => setModal(null)}
        />
      )}
    </div>
  )
}
