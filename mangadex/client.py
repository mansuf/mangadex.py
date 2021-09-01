import aiohttp
import asyncio

class MangaDexClient(aiohttp.ClientSession):
    _lock = asyncio.Lock()

    async def login(self):
        self.get('')
        pass