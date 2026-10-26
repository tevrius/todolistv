from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import engine
from app.exceptions import TaskNotFoundError
from app.routers.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(
    title="TodoList API",
    description="REST API для списка задач: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tasks_router, prefix="/api/v1")


@app.get("/health", tags=["health"], summary="Проверка живости сервиса")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"Задача {exc.task_id} не найдена"},
    )
