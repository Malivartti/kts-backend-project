import asyncio
import logging

import async_timeout
import orjson
from aio_pika import IncomingMessage, Message, connect_robust
from app.store.bot.manager import BotManager
from app.store.tg_api.mappers import dict_to_callback_update, dict_to_update


class RabbitConsumer:
    def __init__(self, bot_manager: BotManager, rabbit_url: str):
        self.bot_manager = bot_manager
        self.rabbit_url = rabbit_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        queue = await self.channel.declare_queue(
            "telegram_updates",
            durable=True,
            arguments={
                "x-max-length": 1000,
                "x-overflow": "reject-publish",
                "x-message-ttl": 10000,
            },
        )
        await queue.consume(self.process_message)

    async def process_message(self, message: IncomingMessage):
        try:
            async with async_timeout.timeout(10):
                update_data = orjson.loads(message.body)
                await self.handle_update(update_data)
                await message.ack()
        except TimeoutError:
            retries = message.headers.get("x-retries", 0)
            new_retries = retries + 1

            if new_retries >= 2:
                logging.error("Message dropped after 2 attempts")
                await message.nack(requeue=False)
            else:
                logging.warning("Timeout error (attempt %d/%d)", new_retries, 2)
                new_headers = dict(message.headers or {})
                new_headers["x-retries"] = new_retries

                await self.channel.default_exchange.publish(
                    Message(
                        body=message.body,
                        content_type=message.content_type,
                        headers=new_headers,
                        delivery_mode=2,
                    ),
                    routing_key="telegram_updates",
                )
                await message.ack()
        except Exception as e:
            logging.exception(
                "Critical error during message processing",
                extra={
                    "error_detail": str(e),
                },
            )
            await message.nack(requeue=False)

    async def handle_update(self, raw_update: dict):
        updates = []
        if "message" in raw_update and "text" in raw_update["message"]:
            updates.append(dict_to_update(raw_update))
        if "callback_query" in raw_update:
            updates.append(dict_to_callback_update(raw_update))

        if updates:
            await self.bot_manager.handle_updates(updates)

    async def start(self):
        await self.connect()
        await asyncio.Future()

    async def stop(self):
        if self.connection:
            await self.connection.close()
