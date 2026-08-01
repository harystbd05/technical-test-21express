class ServiceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundException(ServiceException):
    def __init__(self, message: str = 'Resource not found'):
        super().__init__(message, status_code=404)


class ValidationException(ServiceException):
    def __init__(self, message: str = 'Invalid input data'):
        super().__init__(message, status_code=422)
