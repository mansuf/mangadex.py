# This is experimental ratelimit handler.
# Handle ratelimit properly without constantly checking if we are being rate-limited or not.
# Normal users shouldn't use this, cause this is experimental.

import asyncio
import threading
import logging

log = logging.getLogger(__name__)

# For caching limiters
_stored_rate_limiters = {}

# Global limit requests
_GLOBAL_LIMIT = 300

# for get_rate_limiter()
_lock = threading.Lock()

class _Path:
    def __init__(
        self,
        method: str,
        path: str,
        requests_per_time: int,
        reset_time_in_minutes: int=60
    ) -> None:
        self.METHOD = method
        self.PATH = path
        self.MAX_REQUESTS = requests_per_time
        self.RESET_TIME = reset_time_in_minutes

_RESTRICTED_ENDPOINTS_LIMIT = [
    _Path('POST', '/account/create', 5),
    _Path('POST', '/account/activate/{code}', 30),
    _Path('POST', '/account/activate/resend', 5),
    _Path('POST', '/account/recover', 5),
    _Path('POST', '/account/recover/{code}', 5),
    _Path('POST', '/auth/login', 30),
    _Path('POST', '/auth/refresh', 30),
    _Path('POST', '/author', 10),
    _Path('PUT', '/author', 10),
    _Path('DELETE', '/author/{id}', 10),
    _Path('POST', '/captcha/solve', 10),
    _Path('POST', '/chapter/{id}/read', 300),
    _Path('PUT', '/chapter/{id}', 10),
    _Path('DELETE', '/chapter/{id}', 10),
    _Path('POST', '/manga', 10),
    _Path('PUT', '/manga/{id}', 10),
    _Path('DELETE', '/manga/{id}', 10),
    _Path('POST', '/cover', 10),
    _Path('PUT', '/cover/{id}', 10),
    _Path('DELETE', '/cover/{id}', 10),
    _Path('POST', '/group', 10),
    _Path('PUT', '/group/{id}', 10),
    _Path('DELETE', '/group/{id}', 10),
    _Path('GET', '/at-home/server/{id}', 40, 1),
    _Path('POST', '/report', 10),
    _Path('POST', '/upload/begin', 30)
]

class RateLimiter(asyncio.Semaphore):
    """A built-in ratelimiter for MangaDex API
    without constantly checking if we are being rate limited or not.

    This class implement :class:`asyncio.Semaphore` and thread-safe.
    """
    def __init__(self, path: _Path):
        super().__init__(path.MAX_REQUESTS)
        self._countdown_fut = None
        self._delay = None
        self._path = path
        self._requests_queued = 0
        self.method = path.METHOD
        self.path = path.PATH
        self.requests_limit = path.MAX_REQUESTS
        self.reset_time = path.RESET_TIME * 60 # Convert to seconds from minutes
        self.resetted = asyncio.Event()
        # We are not sending any requests
        self.resetted.set()

        # Thread-safe ratelimiter operations
        self._lock = asyncio.Lock()

    async def _countdown_reset_time(self, delay):
        await asyncio.sleep(delay)
        await self.reset()
        self.resetted.set()
        log.info('Rate limit for "%s %s" is now resetted' % (self.method, self.path))

    async def _wait(self, fut):
        try:
            await fut
        except:
            # See the similar code in Queue.get.
            fut.cancel()
            if self._value > 0 and not fut.cancelled():
                self._wake_up_next()
            raise

    def _create_waiter(self):
        fut = self._loop.create_future()
        self._waiters.append(fut)
        return fut

    async def acquire(self) -> bool:
        print(self._value)
        while self._value <= 0:
            async with self._lock:
                self._requests_queued += 1
            waiter = self._create_waiter()
            log.info('Rate limit is triggered for "%s %s" (requests queued: %s)' % (
                self.method,
                self.path,
                self._requests_queued
            ))
            await self._wait(waiter)

        async with self._lock:
            self._value -= 1
            if self.resetted.is_set():
                delay = self._delay or self.reset_time
                self._start_countdown(delay)
        return True

    def _start_countdown(self, delay):
        # Begin the countdown !!
        log.debug('Starting reset time rate limiter (%ss) countdown' % delay)
        self.resetted.clear()
        self._countdown_fut = asyncio.ensure_future(self._countdown_reset_time(delay))

    async def reboot_rate_limiter(self, requests_remaining, retry_after):
        async with self._lock:
            log.debug('Rate limiter for "%s %s" got reboot with requests_remaining = "%s", retry_after = "%s"' % (
                self.method,
                self.path,
                requests_remaining,
                retry_after
            ))
            if self._countdown_fut is not None:

                # Try to cancel the countdown future
                self._countdown_fut.cancel()
                try:
                    await self._countdown_fut
                except:
                    pass
                self._countdown_fut = None

            # Reboot the rate limiter
            self._value = requests_remaining
            self._reset_without_notify(requests_remaining)
            self._start_countdown(retry_after)

    def _reset_without_notify(self, limit):
        while self._value != limit:
            self._value += 1

    def _wake_up_all(self):
        while self._waiters:
            waiter = self._waiters.popleft()
            if not waiter.done():
                waiter.set_result(None)

    def _reset(self):
        limit = self.requests_limit
        while self._value != limit:
            self._value += 1
            self._wake_up_next()

    async def reset(self) -> None:
        async with self._lock:
            self._reset()

    async def release(self) -> None:
        async with self._lock:
            if self._requests_queued:
                self._requests_queued -= 1

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.release()

def get_rate_limiter(method: str, path: str) -> RateLimiter:
    name = f'{method} {path}'
    with _lock:
        rate_limiter = _stored_rate_limiters.get(name)
        if rate_limiter is None:
            # Create Restricted Ratelimiter if given method and path is endpoints restricted.
            for _path in _RESTRICTED_ENDPOINTS_LIMIT:
                if _path.METHOD == method and path.startswith(_path.PATH):
                    rate_limiter = RateLimiter(_path)
            
            # Create global rate limiter, if given method and path is not endpoint restricted.
            if rate_limiter is None:
                rate_limiter = RateLimiter(_Path(method, path, _GLOBAL_LIMIT, ))
            _stored_rate_limiters[name] = rate_limiter
    return rate_limiter