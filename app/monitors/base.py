from abc import ABC, abstractmethod
from app.services.event_bus import EventBus

class BaseMonitor(ABC):
    def __init__(self, provider_name: str, event_bus: EventBus):
        self.provider_name = provider_name
        self.event_bus = event_bus

    @abstractmethod
    async def run(self):
        pass