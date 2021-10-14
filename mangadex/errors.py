class MangaDexException(BaseException):
    """Base exception for all mangadex error"""
    pass

class NotLoggedIn(MangaDexException):
    """User are not logged in."""
    pass

class ConverterError(MangaDexException):
    """Converter is failing"""
    pass

class HTTPException(MangaDexException):
    """Base exception for HTTP Response in mangadex API."""
    def __init__(self, err: dict) -> None:
        self._id = err.get('id')
        self.status = err.get('status')
        self.title = err.get('title')
        self.detail = err.get('detail')
        self.context = err.get('context')
        fmt = '{0} (code: {1})'
        super().__init__(fmt.format(self.detail, self.status))

class ServerError(HTTPException):
    """Error happened in MangaDex server when performing http request"""
    pass

class Forbidden(HTTPException):
    """Error happened when you don't have permission to do that"""
    pass