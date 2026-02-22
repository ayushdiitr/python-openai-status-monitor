import asyncio
from app.services.event_bus import EventBus
from app.services.logger import Logger
from app.monitors.status import StatusMonitor
from app.config import OPENAI_STATUS_URL, POLL_INTERVAL_SECONDS

async def main():
    event_bus = EventBus()
    logger = Logger()

    event_bus.subscribe(logger.logger)

    monitor = StatusMonitor(
        provider_name="OpenAI",
        base_url=OPENAI_STATUS_URL,
        event_bus=event_bus,
        interval=POLL_INTERVAL_SECONDS
    )

    await monitor.run()


if __name__ == "__main__":
    asyncio.run(main())