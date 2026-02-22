from app.monitors.base import BaseMonitor
from typing import Set, Optional
from app.services.http import HTTPClient
import asyncio
from app.models.incident import Incident
from datetime import datetime

class StatusMonitor(BaseMonitor):
    def __init__(self, provider_name: str, base_url: str, event_bus, interval = 10):
        super().__init__(provider_name, event_bus)
        self.base_url = base_url.rstrip('/')
        self.interval = interval
        self._seen_incidents: Set[str] = set()
        self._etag: Optional[str] = None

    async def run(self):
        async with HTTPClient() as client:
            while True:
                try:
                    url = f"{self.base_url}/api/v2/incidents.json"
                    data, new_etag  = await client.get(url, self._etag)

                    if data is not None:
                        self._etag = new_etag
                        await self._process_incidents(data)

                except Exception as e:
                    print(f"Error in {self.provider_name} monitor: {e}")
                
                await asyncio.sleep(self.interval)

    
    async def _process_incidents(self, data: dict):
        incidents = data.get("incidents", [])

        for incident in incidents:
            incident_name = incident.get("name", "Unknown Service")

            updates = incident.get("incident_updates", [])

            for update in updates:
                update_id = update["id"]

                if update_id in self._seen_incidents:
                    continue

                self._seen_incidents.add(update_id)

                incident_event = Incident(
                    id=update_id,
                    provider=self.provider_name,
                    product=incident_name,
                    status=update.get("status", "unknown"),
                    message=update.get("body", ""),
                    metadata='',
                    created_at=datetime.fromisoformat(
                        update["created_at"].replace("Z", "+00:00")
                    ),
                )

                await self.event_bus.publish(incident_event)