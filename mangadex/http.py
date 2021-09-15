import asyncio
import json
import logging
import aiohttp
import time
from .routes import *
from .errors import Forbidden, HTTPException, ServerError
from .auth import *
from . import __version__

json_dumper = json.dumps

log = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self, *, loop = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self._session = None

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

    async def request(self, route: BaseRoute):
        self.recreate_session()
        params = route.build_request()

        for attempt in range(5):
            try:
                async with self._session.request(**params) as resp:
                    
                    # We are being rate limited
                    if resp.status == 429:
                        
                        # x-ratelimit-retry-after is from MangaDex and
                        # Retry-After is from DDoS-Guard
                        if resp.headers.get('x-ratelimit-retry-after'):
                            delay = float(resp.headers.get('x-ratelimit-retry-after')) - time.time()

                        elif resp.headers.get('Retry-After'):
                            delay = float(resp.headers.get('Retry-After'))

                        await asyncio.sleep(delay)
                        continue
                    
                    # The request was successful
                    elif resp.status == 200:
                        return await resp.json()
                    
                    # Server error
                    elif resp.status >= 500:
                        err = await resp.json()
                        raise ServerError(err)

                    # Forbidden
                    elif resp.status == 403:
                        err = await resp.json()
                        raise Forbidden(err)

                    # 400 and upper.
                    else:
                        err = await resp.json()
                        raise HTTPException(err)

            except OSError:
                await asyncio.sleep(1 + attempt * 2)
                continue

        # We're run out of attempts, throwing error
        raise RuntimeError('Unknown error in HTTP handling')

    # Authentication related

    async def login(self, *args, **kwargs) -> LoginResult:
        data = await self.request(Login(*args, **kwargs))
        return LoginResult(data)

    async def logout(self, session_token) -> LogoutResult:
        data = await self.request(Logout(session_token))
        return LogoutResult(data)

    async def check_token(self, session_token) -> CheckTokenResult:
        data = await self.request(CheckToken(session_token))
        return CheckTokenResult(data)

    async def refresh_token(self, refresh_token) -> RefreshTokenResult:
        data = await self.request(RefreshToken(refresh_token))
        return RefreshTokenResult(data)