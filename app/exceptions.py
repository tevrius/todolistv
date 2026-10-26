import uuid


class TaskNotFoundError(Exception):
    """Задача с указанным идентификатором не найдена."""

    def __init__(self, task_id: uuid.UUID) -> None:
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")
