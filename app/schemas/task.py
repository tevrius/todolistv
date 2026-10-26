import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TaskPriority, TaskStatus

SortField = Literal["created_at", "updated_at", "due_date", "priority", "title"]
SortOrder = Literal["asc", "desc"]


class TaskCreate(BaseModel):
    """Данные для создания задачи."""

    title: str = Field(min_length=1, max_length=200, examples=["Купить хлеб"])
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    category: str | None = Field(default=None, max_length=64, examples=["покупки"])
    due_date: datetime | None = Field(
        default=None, examples=["2026-11-01T18:00:00Z"]
    )


class TaskUpdate(BaseModel):
    """Частичное обновление задачи: передаются только изменяемые поля.

    Явное значение null сбрасывает поле (например, description или category).
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    category: str | None = Field(default=None, max_length=64)
    due_date: datetime | None = None


class TaskRead(BaseModel):
    """Задача в ответах API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    category: str | None
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskPage(BaseModel):
    """Страница списка задач."""

    items: list[TaskRead]
    total: int
    limit: int
    offset: int
