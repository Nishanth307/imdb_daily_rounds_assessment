
class AppException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code 

        super().__init__(message)

class BadRequestException(Exception):
    def __init__(self, message="Bad Request", status_code=400):
        self.message = message
        self.status_code = 400

        super().__init__(message)


class ValidationException(AppException):
    def __init__(self, message="Validation Error", errors=None):
        super().__init__(message, status_code=400)
        self.errors = errors


class NotFoundException(AppException):
    def __init__(self, message="Resource Not Found"):
        super().__init__(message, status_code=404)



class ServerException(AppException):
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, status_code=500)