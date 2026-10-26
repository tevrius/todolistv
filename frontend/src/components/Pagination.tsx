interface PaginationProps {
  total: number
  limit: number
  offset: number
  onPageChange: (page: number) => void
  onLimitChange: (limit: number) => void
}

export function Pagination({ total, limit, offset, onPageChange, onLimitChange }: PaginationProps) {
  const page = Math.floor(offset / limit) + 1
  const totalPages = Math.max(1, Math.ceil(total / limit))

  return (
    <footer className="pagination">
      <span className="pagination__info">Всего: {total}</span>
      <div className="pagination__nav">
        <button
          className="btn"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          ← Назад
        </button>
        <span className="pagination__page">
          Стр. {page} из {totalPages}
        </span>
        <button
          className="btn"
          disabled={page >= totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          Вперёд →
        </button>
      </div>
      <label className="pagination__limit">
        На странице:{' '}
        <select value={limit} onChange={(e) => onLimitChange(Number(e.target.value))}>
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={50}>50</option>
        </select>
      </label>
    </footer>
  )
}
