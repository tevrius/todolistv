import type { FiltersState, SortField, SortOrder, TaskPriority, TaskStatus } from '../types'
import { PRIORITY_LABELS, SORT_FIELD_LABELS, SORT_ORDER_LABELS, STATUS_LABELS } from '../utils/labels'

interface FiltersBarProps {
  filters: FiltersState
  categories: string[]
  onChange: (partial: Partial<FiltersState>) => void
  onReset: () => void
}

export function FiltersBar({ filters, categories, onChange, onReset }: FiltersBarProps) {
  const hasActiveFilters =
    filters.status !== '' ||
    filters.priority !== '' ||
    filters.category !== '' ||
    filters.search !== '' ||
    filters.sortBy !== 'created_at' ||
    filters.sortOrder !== 'desc'

  return (
    <section className="filters">
      <label className="field">
        <span className="field__label">Поиск</span>
        <input
          type="search"
          placeholder="По названию…"
          maxLength={200}
          value={filters.search}
          onChange={(e) => onChange({ search: e.target.value })}
        />
      </label>

      <label className="field">
        <span className="field__label">Статус</span>
        <select
          value={filters.status}
          onChange={(e) => onChange({ status: e.target.value as TaskStatus | '' })}
        >
          <option value="">Все</option>
          {(Object.keys(STATUS_LABELS) as TaskStatus[]).map((s) => (
            <option key={s} value={s}>
              {STATUS_LABELS[s]}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span className="field__label">Приоритет</span>
        <select
          value={filters.priority}
          onChange={(e) => onChange({ priority: e.target.value as TaskPriority | '' })}
        >
          <option value="">Все</option>
          {(Object.keys(PRIORITY_LABELS) as TaskPriority[]).map((p) => (
            <option key={p} value={p}>
              {PRIORITY_LABELS[p]}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span className="field__label">Категория</span>
        <select
          value={filters.category}
          onChange={(e) => onChange({ category: e.target.value })}
        >
          <option value="">Все</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span className="field__label">Сортировка</span>
        <select
          value={filters.sortBy}
          onChange={(e) => onChange({ sortBy: e.target.value as SortField })}
        >
          {(Object.keys(SORT_FIELD_LABELS) as SortField[]).map((f) => (
            <option key={f} value={f}>
              {SORT_FIELD_LABELS[f]}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span className="field__label">Порядок</span>
        <select
          value={filters.sortOrder}
          onChange={(e) => onChange({ sortOrder: e.target.value as SortOrder })}
        >
          <option value="desc">{SORT_ORDER_LABELS.desc}</option>
          <option value="asc">{SORT_ORDER_LABELS.asc}</option>
        </select>
      </label>

      {hasActiveFilters && (
        <button className="btn btn--link filters__reset" onClick={onReset}>
          Сбросить фильтры
        </button>
      )}
    </section>
  )
}
