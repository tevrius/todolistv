"""initial tasks table

Revision ID: 0001
Revises:
Create Date: 2026-10-26

"""
import enum
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from app.models.task import TaskPriority, TaskStatus

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def enum_column(enum_cls: type[enum.StrEnum], name: str) -> sa.Enum:
    """Enum-колонка, соответствующая описанию в app/models/task.py."""
    return sa.Enum(
        enum_cls,
        name=name,
        native_enum=False,
        length=32,
        values_callable=lambda e: [member.value for member in e],
    )


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", enum_column(TaskStatus, "task_status"), nullable=False),
        sa.Column("priority", enum_column(TaskPriority, "task_priority"), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_category"), "tasks", ["category"])
    op.create_index(op.f("ix_tasks_due_date"), "tasks", ["due_date"])


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_due_date"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_category"), table_name="tasks")
    op.drop_table("tasks")
