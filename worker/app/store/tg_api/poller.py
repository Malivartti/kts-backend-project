from asyncio import Task, create_task

from app.store import Store


class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        self.is_running = True
        self.poll_task = create_task(self.poll())

    async def stop(self) -> None:
        self.is_running = False
        if self.poll_task:
            self.poll_task.cancel()

    async def poll(self) -> None:
        while self.is_running:
            updates = await self.store.tg_api.poll()

            if updates:
                await self.store.bot_manager.handle_updates(updates)
