import asyncio

from app.base.base_accessor import BaseAccessor
from app.store.queue.consumer import RabbitConsumer
from app.web.app import Application


class QueueAccessor(BaseAccessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumer_task: asyncio.Task | None = None

    async def connect(self, _: "Application"):
        rabbit_url = (
            f"amqp://{self.app.config.rabbitmq.user}:"
            f"{self.app.config.rabbitmq.password}@"
            f"{self.app.config.rabbitmq.host}/"
        )
        self.rabbit_consumer = RabbitConsumer(
            bot_manager=self.app.store.bot_manager,
            rabbit_url=rabbit_url,
        )
        self.consumer_task = asyncio.create_task(self.rabbit_consumer.start())

    async def disconnect(self, _: "Application"):
        if self.rabbit_consumer:
            if self.consumer_task and not self.consumer_task.done():
                self.consumer_task.cancel()
                try:
                    await self.consumer_task
                except asyncio.CancelledError:
                    pass
            await self.rabbit_consumer.stop()
