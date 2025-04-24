import asyncio
import logging
import os
import signal
from urllib.parse import urlencode

import orjson
from aio_pika import Message, connect_robust
from aiohttp import ClientSession


class Poller:
    def __init__(self, token: str, rabbit_url: str):
        self.token = token
        self.rabbit_url = rabbit_url
        self.offset = None
        self.session = None
        self.connection = None
        self.channel = None
        self.queue = None
        self.running = True
        self.max_queue_size = 500
        self.polling_interval = 0.1
        self.backoff_interval = 5

    async def connect(self):
        self.session = ClientSession()
        self.connection = await connect_robust(self.rabbit_url)
        self.channel = await self.connection.channel()

        await self.channel.set_qos(prefetch_count=5)

        self.queue = await self.channel.declare_queue(
            "telegram_updates",
            durable=True,
            arguments={
                "x-max-length": 1000,
                "x-overflow": "reject-publish",
                "x-message-ttl": 10000,
            },
        )

        logging.info("Poller connected to RabbitMQ and ready to fetch updates")

    async def _build_url(self, method: str, params: dict) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}?{urlencode(params)}"

    async def fetch_updates(self):
        params = {"timeout": 25}
        if self.offset:
            params["offset"] = self.offset

        url = await self._build_url("getUpdates", params)
        try:
            async with self.session.get(url) as response:
                data = await response.json()
                if not data.get("ok"):
                    logging.error("Polling error: %s", data.get("description"))
                    return []

                updates = []
                for update in data.get("result", []):
                    updates.append(update)
                    self.offset = max(self.offset or 0, update["update_id"] + 1)

                return updates
        except TimeoutError:
            logging.warning("Timeout while fetching updates from Telegram API")
            return []
        except Exception as e:
            logging.exception(
                "Error fetching updates", extra={"error_detail": str(e)}
            )
            return []

    async def publish_update(self, update: dict):
        try:
            message = Message(
                body=orjson.dumps(update),
                content_type="application/json",
                headers={"X-Update-Type": "telegram"},
                delivery_mode=2,  # Persistent
            )

            update_id = update.get("update_id", "unknown")

            await self.channel.default_exchange.publish(
                message, routing_key="telegram_updates", timeout=5
            )
            logging.debug("Published update %s to RabbitMQ", update_id)
        except Exception as e:
            logging.exception(
                "Failed to publish update %s",
                update.get("update_id", "unknown"),
                extra={"error_detail": str(e)},
            )

    async def check_queue_size(self):
        message_count = 0
        try:
            message_count = self.queue.declaration_result.message_count

            if message_count > 100:
                logging.info("Current queue size: %s messages", message_count)

        except Exception as e:
            logging.exception(
                "Failed to check queue size", extra={"error_detail": str(e)}
            )

        return message_count

    async def setup_signal_handlers(self):
        loop = asyncio.get_running_loop()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                sig, lambda: asyncio.create_task(self.shutdown())
            )

        logging.info("Signal handlers configured")

    async def shutdown(self):
        logging.info("Shutting down poller...")
        self.running = False

        if self.connection:
            await self.connection.close()
            logging.info("RabbitMQ connection closed")

        if self.session:
            await self.session.close()
            logging.info("HTTP session closed")

        logging.info("Poller shutdown complete")

    async def run(self):
        await self.connect()
        await self.setup_signal_handlers()

        logging.info("Starting Telegram polling loop")

        while self.running:
            try:
                queue_size = await self.check_queue_size()

                if queue_size > self.max_queue_size:
                    logging.warning(
                        "Queue backlog: %s messages. "
                        "Pausing polling for %s seconds.",
                        queue_size,
                        self.backoff_interval,
                    )
                    await asyncio.sleep(self.backoff_interval)
                    continue

                updates = await self.fetch_updates()

                for update in updates:
                    await self.publish_update(update)

                await asyncio.sleep(self.polling_interval)

            except asyncio.CancelledError:
                logging.info("Polling task cancelled")
                break
            except Exception as e:
                logging.exception(
                    "Unexpected error in polling loop",
                    extra={"error_detail": str(e)},
                )

                await asyncio.sleep(3)

        await self.shutdown()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    rabbit_user = os.getenv("RABBITMQ_DEFAULT_USER")
    rabbit_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
    rabbit_host = os.getenv("RABBITMQ_HOST")
    rabbit_url = f"amqp://{rabbit_user}:{rabbit_pass}@{rabbit_host}/"

    poller = Poller(token=os.getenv("TG_BOT_TOKEN"), rabbit_url=rabbit_url)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(poller.run())
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, shutting down")
    finally:
        pending = asyncio.all_tasks(loop=loop)
        loop.run_until_complete(
            asyncio.gather(*pending, return_exceptions=True)
        )
        loop.close()
        logging.info("Poller process terminated")
