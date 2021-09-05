import asyncio
import logging
import aiohttp
import sys
import time
from .ratelimiter import get_rate_limiter
from .errors import HTTPException
from . import __version__

try:
    from orjson import dumps
    json_dumper = dumps
except ImportError:
    from json import dumps
    json_dumper = dumps

log = logging.getLogger(__name__)

class Route:
    BASE = 'https://api.mangadex.org'

    def __init__(self, method: str, path: str, **params) -> None:
        self.method = method
        self.path = path
        self.absolute_path = path.format(**params)
        self.url = self.BASE + self.absolute_path

class HTTPClient:
    def __init__(self, *, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self._session = None
        user_agent = 'mangadex.py (https://github.com/mansuf/mangadex.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    def _create_session(self):
        self._session = aiohttp.ClientSession(json_serialize=json_dumper, loop=self.loop)

    def recreate_session(self):
        if not self._session:
            self._create_session()
        if self._session.closed:
            self._create_session()

    async def close_session(self):
        if self._session:
            await self._session.close()

    async def request(self, route: Route, **params):
        self.recreate_session()

        path = route.absolute_path
        url = route.url
        method = route.method

        # Set up headers
        headers = {
            "User-Agent": self.user_agent
        }
        params['headers'] = headers
        
        # Check if request is json encoded
        if params.get('json') is not None:
            headers["Content-Type"] = "application/json"

        # Get limiter requests
        limiter = get_rate_limiter(method, path)

        # Begin request
        for attempt in range(5):
            async with limiter:
                try:
                    async with self._session.request(method, url, **params) as resp:

                        # We are being rate-limited
                        if resp.status == 429:
                            print(await resp.json())
                            retry_after = resp.headers.get('x-ratelimit-retry-after') or resp.headers.get('Retry-After')
                            delay_remaining = float(retry_after) - time.time()
                            ratelimit_remaining = int(resp.headers['x-ratelimit-remaining'])
                            await limiter.reboot_rate_limiter(ratelimit_remaining, delay_remaining)
                            continue
                        
                        if resp.status == 200:
                            return await resp.json()
                except OSError:
                    pass
        # We're run out of attempts, throwing error
        return None
                



    # Authentication related

    def login(self):
        pass