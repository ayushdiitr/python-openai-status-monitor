from app.models.incident import Incident    

class Logger:
    async def logger(self, incident: Incident) -> None:
        print(
            f"[{incident.created_at}] "
            f"Product: {incident.product}\n"
            f"Status: {incident.status}\n"
        )