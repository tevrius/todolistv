const dateTimeFormatter = new Intl.DateTimeFormat('ru-RU', {
  dateStyle: 'medium',
  timeStyle: 'short',
})

/** ISO-строка из API -> человекочитаемый формат, null -> прочерк */
export function formatDateTime(iso: string | null): string {
  if (!iso) return '—'
  return dateTimeFormatter.format(new Date(iso))
}

/** ISO-строка из API -> значение для <input type="datetime-local"> */
export function toInputValue(iso: string | null): string {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

/** Значение datetime-local -> ISO-строка для API */
export function fromInputValue(value: string): string | null {
  if (!value) return null
  return new Date(value).toISOString()
}

/** Просрочена ли задача (срок в прошлом и не выполнена) */
export function isOverdue(dueIso: string | null, done: boolean): boolean {
  if (!dueIso || done) return false
  return new Date(dueIso).getTime() < Date.now()
}
