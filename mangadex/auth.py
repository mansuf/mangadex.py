from typing import List

__all__ = (
    'LoginResult', 'CheckTokenResult',
    'LogoutResult', 'RefreshTokenResult'
)

class AuthResult:
    def __init__(self, data) -> None:
        self._data = data

    def __bool__(self) -> bool:
        return True if self._data.get('result') == 'ok' else False

class Token(AuthResult):
    def __init__(self, data) -> None:
        super().__init__(data)
        self._token = data.get('token')

    @property
    def session_token(self) -> str:
        return self._token.get('session')

    @property
    def refresh_token(self) -> str:
        return self._token.get('refresh')

class LoginResult(Token):
    pass

class CheckTokenResult(AuthResult):
    def __bool__(self) -> bool:
        return self._data.get('isAuthenticated')
    
    @property
    def roles(self) -> List[str]:
        return self._data.get('roles')

    @property
    def permissions(self) -> List[str]:
        return self._data.get('permissions')

class LogoutResult(AuthResult):
    pass

class RefreshTokenResult(Token):
    @property
    def message(self) -> str:
        return self._data.get('message')


