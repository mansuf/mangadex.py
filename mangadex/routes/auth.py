import re
from .base import GET, POST, RequireLogin

__all__ = (
    'Login', 'CheckToken',
    'RefreshToken', 'Logout'
)

class Login(POST):
    path = '/auth/login'

    def __init__(self, password: str, username: str=None, email: str=None) -> None:
        # verify password
        if not isinstance(password, str):
            raise ValueError('password must be str')
        else:
            length_password = len(password)
            if length_password < 8:
                raise ValueError("password must be 8 characters long")
            elif length_password > 1024:
                raise ValueError('password cannot be more than 1024 characters long')
            self.password = password
        
        # check if username and email is empty
        # if yes, raise error
        if username is None and email is None:
            raise ValueError('at least provide a username or an email to login')
        
        # verify username
        if username:
            if not isinstance(username, str):
                raise ValueError('username must be str')
            else:
                if len(username) > 64 or len(username) <= 0:
                    raise ValueError('username characters range must be from 1 to 64')
        self.username = username

        # verify email
        # Adapted from https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
        re_email = re.compile(r'^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$', re.IGNORECASE)
        if email:
            if not isinstance(email, str):
                raise ValueError('email must be str')
            else:
                if re_email.match(email) is None:
                    raise ValueError('"%s" is not valid email' % email)
        self.email = email

    def build_request(self):
        request_params = super().build_request(self.path)
        data = {}
        request_params['json'] = data

        data['password'] = self.password

        if self.username:
            data['username'] = self.username

        if self.email:
            data['email'] = self.email
        
        return request_params

class CheckToken(GET, RequireLogin):
    path = '/auth/check'
    
    def __init__(self, session_token: str) -> None:
        self.set_auth_token(session_token)

    def build_request(self):
        return super().build_request(self.path)

class Logout(POST, RequireLogin):
    path = '/auth/logout'

    def __init__(self, session_token: str) -> None:
        self.set_auth_token(session_token)

    def build_request(self):
        return super().build_request(self.path)

class RefreshToken(POST):
    path = '/auth/refresh'

    def __init__(self, refresh_token: str) -> None:
        if not isinstance(refresh_token, str):
            raise ValueError('token must be str')
        self.token = refresh_token

    def build_request(self):
        request_params = super().build_request(self.path)
        request_params['json'] = {'token': self.token}
        return request_params