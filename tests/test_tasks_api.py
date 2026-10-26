"""Интеграционные тесты API задач.

Выполняются на SQLite (aiosqlite), поэтому для запуска не нужен PostgreSQL:
    uv run pytest
"""

import uuid

from httpx import AsyncClient

BASE = "/api/v1/tasks"


async def create_task(client: AsyncClient, **overrides: object) -> dict:
    payload: dict = {
        "title": "Задача",
        "description": "Описание",
        "priority": "medium",
        "category": "home",
    }
    payload.update(overrides)
    response = await client.post(BASE, json=payload)
    assert response.status_code == 201, response.text
    return response.json()


async def test_create_task_defaults(client: AsyncClient) -> None:
    response = await client.post(BASE, json={"title": "Купить хлеб"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Купить хлеб"
    assert body["status"] == "todo"
    assert body["priority"] == "medium"
    assert body["description"] is None
    assert body["due_date"] is None
    uuid.UUID(body["id"])  # id — валидный UUID
    assert body["created_at"]
    assert body["updated_at"]


async def test_get_task(client: AsyncClient) -> None:
    created = await create_task(client)
    response = await client.get(f"{BASE}/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


async def test_get_missing_task(client: AsyncClient) -> None:
    response = await client.get(f"{BASE}/{uuid.uuid4()}")
    assert response.status_code == 404
    assert "не найдена" in response.json()["detail"]


async def test_list_filters_and_pagination(client: AsyncClient) -> None:
    await create_task(client, title="A", status="todo", priority="high", category="work")
    await create_task(client, title="B", status="done", priority="low", category="home")
    await create_task(client, title="C отчёт", status="todo", priority="medium", category="work")

    body = (await client.get(BASE)).json()
    assert body["total"] == 3
    assert len(body["items"]) == 3

    assert (await client.get(BASE, params={"status": "todo"})).json()["total"] == 2
    assert (await client.get(BASE, params={"status": "done"})).json()["total"] == 1
    assert (await client.get(BASE, params={"priority": "low"})).json()["total"] == 1
    assert (await client.get(BASE, params={"category": "work"})).json()["total"] == 2
    assert (await client.get(BASE, params={"search": "отчёт"})).json()["total"] == 1
    assert (await client.get(BASE, params={"search": "неттакой"})).json()["total"] == 0

    # Комбинация фильтров + пагинация + сортировка
    body = (
        await client.get(
            BASE,
            params={"status": "todo", "category": "work", "limit": 1, "offset": 0,
                    "sort_by": "title", "sort_order": "asc"},
        )
    ).json()
    assert body["total"] == 2
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "A"
    assert body["limit"] == 1
    assert body["offset"] == 0


async def test_list_sort_by_priority(client: AsyncClient) -> None:
    await create_task(client, title="high", priority="high")
    await create_task(client, title="low", priority="low")
    await create_task(client, title="medium", priority="medium")

    asc = (await client.get(BASE, params={"sort_by": "priority", "sort_order": "asc"})).json()
    assert [t["priority"] for t in asc["items"]] == ["low", "medium", "high"]

    desc = (await client.get(BASE, params={"sort_by": "priority", "sort_order": "desc"})).json()
    assert [t["priority"] for t in desc["items"]] == ["high", "medium", "low"]


async def test_update_task(client: AsyncClient) -> None:
    created = await create_task(client, description="old")

    response = await client.patch(
        f"{BASE}/{created['id']}", json={"status": "done", "priority": "high"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "done"
    assert body["priority"] == "high"
    assert body["title"] == "Задача"  # не передавалось — не изменилось
    assert body["description"] == "old"

    # Явный null сбрасывает поле
    response = await client.patch(f"{BASE}/{created['id']}", json={"description": None})
    assert response.status_code == 200
    assert response.json()["description"] is None


async def test_update_missing_task(client: AsyncClient) -> None:
    response = await client.patch(f"{BASE}/{uuid.uuid4()}", json={"title": "x"})
    assert response.status_code == 404


async def test_delete_task(client: AsyncClient) -> None:
    created = await create_task(client)
    response = await client.delete(f"{BASE}/{created['id']}")
    assert response.status_code == 204

    response = await client.get(f"{BASE}/{created['id']}")
    assert response.status_code == 404


async def test_validation_errors(client: AsyncClient) -> None:
    assert (await client.post(BASE, json={"title": ""})).status_code == 422
    assert (
        await client.post(BASE, json={"title": "x", "priority": "urgent"})
    ).status_code == 422
    assert (
        await client.post(BASE, json={"title": "x", "status": "unknown"})
    ).status_code == 422
    assert (await client.get(f"{BASE}/не-uuid")).status_code == 422


async def test_categories(client: AsyncClient) -> None:
    await create_task(client, category="work")
    await create_task(client, category="home")
    await create_task(client, category=None)

    response = await client.get(f"{BASE}/categories")
    assert response.status_code == 200
    assert response.json() == ["home", "work"]


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
