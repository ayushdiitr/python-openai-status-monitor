from typing import Callable, List, Awaitable
from app.models.incident import Incident

class EventBus:
    def __init__(self):
        self._subscribers: List[Callable[[Incident], Awaitable[None]]] = []

    def subscribe(self, handler: Callable[[Incident], Awaitable[None]]) -> None:
        self._subscribers.append(handler)

    async def publish(self, incident: Incident) -> None:
        for i in self._subscribers:
            await i(incident)