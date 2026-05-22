"""Главный файл программы для запуска."""
import asyncio
import uvicorn

from src.app import create_app
from fastapi.staticfiles import StaticFiles
from pathlib import Path


BASE_DIR = Path("/app")

app = create_app()
app.mount("/media", StaticFiles(directory=str(BASE_DIR / "media")), name="media")


async def run() -> None:
    """Ассинхронная функция для запуска приложения."""
    config = uvicorn.Config(
        "main:app", host="0.0.0.0", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
