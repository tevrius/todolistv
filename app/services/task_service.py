import uuid

from app.exceptions import TaskNotFoundError
from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import SortField, SortOrder, TaskCreate, TaskUpdate


class TaskService:
    """Бизнес-логика работы с задачами."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def create(self, data: TaskCreate) -> Task:
        return await self._repository.create(**data.model_dump())

    async def get(self, task_id: uuid.UUID) -> Task:
        task = await self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        category: str | None = None,
        search: str | None = None,
        sort_by: SortField = "created_at",
        sort_order: SortOrder = "desc",
        limit: int,
        offset: int,
    ) -> tuple[list[Task], int]:
        return await self._repository.list_tasks(
            status=status,
            priority=priority,
            category=category,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
        )

    async def update(self, task_id: uuid.UUID, data: TaskUpdate) -> Task:
        task = await self.get(task_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        return task

    async def delete(self, task_id: uuid.UUID) -> None:
        task = await self.get(task_id)
        await self._repository.delete(task)

    async def categories(self) -> list[str]:
        return await self._repository.categories()
