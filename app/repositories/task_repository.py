import uuid

from sqlalchemy import Select, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import SortField, SortOrder


class TaskRepository:
    """Доступ к данным задач: только запросы к БД, без бизнес-логики."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, **fields: object) -> Task:
        task = Task(**fields)  # type: ignore[arg-type]
        self._session.add(task)
        await self._session.flush()
        return task

    async def get(self, task_id: uuid.UUID) -> Task | None:
        return await self._session.get(Task, task_id)

    async def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        category: str | None = None,
        search: str | None = None,
        sort_by: SortField = "created_at",
        sort_order: SortOrder = "desc",
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Task], int]:
        """Список задач с фильтрацией, сортировкой и пагинацией.

        Возвращает кортеж (страница задач, общее количество подходящих задач).
        """
        conditions = []
        if status is not None:
            conditions.append(Task.status == status)
        if priority is not None:
            conditions.append(Task.priority == priority)
        if category is not None:
            conditions.append(Task.category == category)
        if search:
            conditions.append(Task.title.ilike(f"%{search}%"))

        stmt: Select = (
            select(Task)
            .where(*conditions)
            .order_by(self._order_by(sort_by, sort_order))
            .limit(limit)
            .offset(offset)
        )
        tasks = list((await self._session.scalars(stmt)).all())

        count_stmt = select(func.count()).select_from(Task).where(*conditions)
        total = await self._session.scalar(count_stmt)
        return tasks, total or 0

    async def delete(self, task: Task) -> None:
        await self._session.delete(task)
        await self._session.flush()

    async def categories(self) -> list[str]:
        """Все различные непустые категории (для фильтра на клиенте)."""
        stmt = (
            select(Task.category)
            .where(Task.category.is_not(None))
            .distinct()
            .order_by(Task.category)
        )
        return list((await self._session.scalars(stmt)).all())

    @staticmethod
    def _order_by(sort_by: SortField, sort_order: SortOrder) -> object:
        column = getattr(Task, sort_by)
        if sort_by == "priority":
            # Сортировка по смысловой важности, а не по алфавиту значений
            column = case(
                (Task.priority == TaskPriority.LOW, 0),
                (Task.priority == TaskPriority.MEDIUM, 1),
                else_=2,
            )
        return column.desc() if sort_order == "desc" else column.asc()
