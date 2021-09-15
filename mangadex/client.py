import asyncio
from .http import HTTPClient
from .routes import *
from .errors import *

class Client:
    """MangaDex Client
    
    Parameters
    -----------
    loop: :class:`asyncio.AbstractEventLoop`
        Set asyncio event loop.
    auto_refresh_session: :class:`bool`
        If this ``True`` the session will be refreshed each time user do action
        that require authentication (except for login and logout).
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        auto_refresh_session: bool = True
    ) -> None:
        self._session_token = None
        self._refresh_token = None
        self._auto_refresh_session = auto_refresh_session
        self._logged_in = asyncio.Event()
        self._http = HTTPClient(loop=loop)

        # For thread-safe operations login and logout
        self._auth_lock = asyncio.Lock()

    async def login(self, *args, **kwargs):
        """Login to MangaDex

        Email or username and password is required for login.

        Note
        -----
        If already logged in, it will refresh the session using "refresh token" and
        if failed to refresh the session, password and username will be used for log in.
        
        Parameters
        -----------
        password: :class:`str`
            Password credential for login.
        username: Union[:class:`str`, ``None``]
            Username credential for login. (default to ``None``)
        email: Union[:class:`str`, ``None``]
            Email credential for login. (default to ``None``)

        Raises
        -------
        HTTPException
            Username, email or password is invalid
        """
        async with self._auth_lock:
            if self._logged_in.is_set():
                # Check if current session token is valid
                if await self._http.check_token(self._session_token):
                    self._logged_in.clear()

                    # If not valid, refresh it
                    result = await self._http.refresh_token(self._refresh_token)
                    self._session_token = result.session_token
                    self._refresh_token = result.refresh_token
                    self._logged_in.set()
                    return

            # Log in
            result = await self._http.login(*args, **kwargs)

            # Set session and refresh token
            self._session_token = result.session_token
            self._refresh_token = result.refresh_token

            # We are logged in
            self._logged_in.set()
    
    async def logout(self):
        """Logout from MangaDex
        
        Raises
        -------
        NotLoggedIn
            You are not logged in
        HTTPException
            Invalid session token
        """
        async with self._auth_lock:
            if not self._logged_in.is_set():
                raise NotLoggedIn('You are not logged in')
            await self._http.logout(self._session_token)
            self._logged_in.clear()