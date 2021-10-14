import sys
import aiohttp
from .. import __version__

__all__ = (
    'BaseRoute', 'RequireLogin', 'GET',
    'POST', 'PUT', 'DELETE',
)

class BaseRoute:
    BASE_URL = 'https://api.mangadex.org'
    user_agent = 'mangadex.py (https://github.com/mansuf/mangadex.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'.format(
        __version__, sys.version_info, aiohttp.__version__
    )
    headers = {"User-Agent": user_agent}

    def build_request(self, path: str):
        return {
            "method": self.method,
            "url": self.BASE_URL + path,
            "headers": self.headers
        }

class RequireLogin:
    def set_auth_token(self, token: str):
        if not isinstance(token, str):
            raise ValueError('token must be str')
        
        self.headers['Authorization'] = f'Bearer {token}'

class GET(BaseRoute):
    method = 'GET'

class POST(BaseRoute):
    method = 'POST'

class PUT(BaseRoute):
    method = 'PUT'

class DELETE(BaseRoute):
    method = 'DELETE'