import aiohttp
from typing import Optional

class HTTPClient:
    def __init__(self, timeout:int = 10):
        self._timeout = aiohttp.ClientTimeout(timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(timeout=self._timeout)
        return self
    
    async def __aexit__(self, *args):
        await self._session.close()

    async def get(self, url: str, etag: Optional[str] = None):
        headers = {}
        if etag: 
            headers["If-None-Match"] = etag

        async with self._session.get(url, headers=headers) as response:
            if response.status == 304:
                return None, etag
            
            response.raise_for_status()
            new_etag = response.headers.get("ETAG")
            data = await response.json()
            return data, new_etag