import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import (
    SortField,
    SortOrder,
    TaskCreate,
    TaskPage,
    TaskRead,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(session: Annotated[AsyncSession, Depends(get_session)]) -> TaskService:
    return TaskService(TaskRepository(session))


ServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.post("", response_model=TaskRead, status_code=201, summary="Создать задачу")
async def create_task(data: TaskCreate, service: ServiceDep) -> Task:
    return await service.create(data)


@router.get("", response_model=TaskPage, summary="Список задач с фильтрами")
async def list_tasks(
    service: ServiceDep,
    status: TaskStatus | None = Query(default=None, description="Фильтр по статусу"),
    priority: TaskPriority | None = Query(default=None, description="Фильтр по приоритету"),
    category: str | None = Query(default=None, max_length=64, description="Фильтр по категории"),
    search: str | None = Query(
        default=None, min_length=1, max_length=200, description="Поиск по названию"
    ),
    limit: int = Query(default=20, ge=1, le=100, description="Размер страницы"),
    offset: int = Query(default=0, ge=0, description="Смещение"),
    sort_by: SortField = Query(default="created_at", description="Поле сортировки"),
    sort_order: SortOrder = Query(default="desc", description="Направление сортировки"),
) -> TaskPage:
    items, total = await service.list_tasks(
        status=status,
        priority=priority,
        category=category,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )
    return TaskPage(items=items, total=total, limit=limit, offset=offset)


@router.get("/categories", response_model=list[str], summary="Список категорий")
async def list_categories(service: ServiceDep) -> list[str]:
    return await service.categories()


@router.get("/{task_id}", response_model=TaskRead, summary="Получить задачу")
async def get_task(task_id: uuid.UUID, service: ServiceDep) -> Task:
    return await service.get(task_id)


@router.patch("/{task_id}", response_model=TaskRead, summary="Обновить задачу")
async def update_task(task_id: uuid.UUID, data: TaskUpdate, service: ServiceDep) -> Task:
    return await service.update(task_id, data)


@router.delete("/{task_id}", status_code=204, summary="Удалить задачу")
async def delete_task(task_id: uuid.UUID, service: ServiceDep) -> None:
    await service.delete(task_id)
