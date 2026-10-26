# TodoList

Полноценный todo-list: **FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL + Alembic** на бэкенде, **React + TypeScript + Vite + TanStack Query** на фронтенде. Управление зависимостями: **uv** (Python) и **npm** (JS). Всё разворачивается в **Docker**.

## Возможности

- CRUD задач: создание, просмотр, частичное обновление (PATCH), удаление
- Статусы (`todo`, `in_progress`, `done`), приоритеты (`low`, `medium`, `high`), категории, дедлайны
- Фильтрация по статусу/приоритету/категории, поиск по названию
- Сортировка и пагинация
- Веб-интерфейс: список задач, фильтры, модальное окно создания/редактирования, отметка выполнения чекбоксом, подтверждение удаления
- Автодокументация API: Swagger UI (`/docs`) и ReDoc (`/redoc`)

## Структура проекта

```
app/                   # бэкенд (FastAPI)
  config.py            # настройки (pydantic-settings, .env)
  database.py          # async-движок, сессии, Base
  exceptions.py        # доменные исключения
  models/task.py       # ORM-модель Task, enum'ы
  schemas/task.py      # Pydantic-схемы запросов/ответов
  repositories/        # доступ к данным (запросы к БД)
  services/            # бизнес-логика
  routers/             # HTTP-эндпоинты
  main.py              # сборка приложения
migrations/            # миграции Alembic
frontend/              # фронтенд (React + Vite)
  src/api/             # fetch-клиент и запросы к API
  src/hooks/           # TanStack Query хуки, debounce
  src/components/      # список задач, фильтры, модалка, пагинация
  src/utils/           # форматирование дат, подписи enum'ов
  nginx.conf           # прод: статика + прокси /api на бэкенд
tests/                 # интеграционные тесты API (на SQLite, Postgres не нужен)
```

## Требования

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`)
- [Docker](https://docs.docker.com/) — для PostgreSQL и прод-запуска
- [Node.js 20+](https://nodejs.org/) — только для разработки фронтенда

## Быстрый старт в Docker (всё в одном)

```bash
docker compose up --build
```

Поднимутся PostgreSQL, API (миграции применяются автоматически) и фронтенд.

- Веб-интерфейс: http://localhost:3000
- API docs: http://localhost:8001/docs
- Health: http://localhost:8001/health

Остановить: `docker compose down` (данные БД сохраняются в томе `pgdata`; чтобы удалить их полностью — `docker compose down -v`).

## Локальный запуск (uv + Vite dev)

```bash
# Бэкенд
uv sync                                # установить зависимости
copy .env.example .env                 # настроить DATABASE_URL при необходимости
docker compose up -d db                # поднять только PostgreSQL
uv run alembic upgrade head            # применить миграции
uv run uvicorn app.main:app --reload   # API на http://localhost:8001

# Фронтенд (в новом терминале)
cd frontend
npm install
npm run dev                            # UI на http://localhost:5173 (прокси /api на :8001)
```

## Тесты

Тесты API используют SQLite (aiosqlite), PostgreSQL для них не нужен:

```bash
uv run pytest
```

## API

Базовый префикс: `/api/v1` (с фронтенда запросы идут на тот же origin — их проксируют Vite dev-server или nginx)

| Метод   | Путь                        | Описание                                              |
|---------|-----------------------------|-------------------------------------------------------|
| POST    | `/api/v1/tasks`             | Создать задачу                                        |
| GET     | `/api/v1/tasks`             | Список задач (фильтры, поиск, сортировка, пагинация)  |
| GET     | `/api/v1/tasks/categories`  | Различные категории (для фильтра на клиенте)          |
| GET     | `/api/v1/tasks/{id}`        | Получить задачу                                       |
| PATCH   | `/api/v1/tasks/{id}`        | Частично обновить задачу (null сбрасывает поле)       |
| DELETE  | `/api/v1/tasks/{id}`        | Удалить задачу                                        |
| GET     | `/health`                   | Проверка живости сервиса                              |

Параметры списка: `status`, `priority`, `category`, `search`, `limit` (1–100, по умолчанию 20), `offset`, `sort_by` (`created_at`, `updated_at`, `due_date`, `priority`, `title`), `sort_order` (`asc`/`desc`).

### Примеры (curl)

```bash
# Создать задачу
curl -X POST http://localhost:8001/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить хлеб", "priority": "high", "category": "покупки", "due_date": "2026-11-01T18:00:00Z"}'

# Список незавершённых задач с высоким приоритетом
curl "http://localhost:8001/api/v1/tasks?status=todo&priority=high&sort_by=due_date&sort_order=asc"

# Отметить как выполненную
curl -X PATCH http://localhost:8001/api/v1/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'

# Удалить
curl -X DELETE http://localhost:8001/api/v1/tasks/<id>
```

## Миграции

```bash
# Создать автогенерируемую миграцию после изменения моделей
uv run alembic revision --autogenerate -m "описание изменений"

# Применить / откатить
uv run alembic upgrade head
uv run alembic downgrade base

# Посмотреть текущую и историю ревизий
uv run alembic current
uv run alembic history
```

## Полезные команды

```bash
uv run pytest                 # тесты API
npm run dev                   # фронтенд в dev-режиме (из папки frontend/)
npm run build                 # прод-сборка фронтенда (из папки frontend/)
docker compose up --build     # полный стек: db + api + frontend
docker compose up -d db       # только PostgreSQL
docker compose logs -f app    # логи API
```
