class BaseException(Exception):
    """Basic initialization exception class."""

    def __init__(self, message, description) -> None:
        """Initializing custom exception class."""
        self.description = description
        if message:
            self.message = message
        else:
            self.message = None

    def __str__(self):
        """Basic exceprion error message."""
        if self.message:
            return f'''
        {self.__class__.__name__}
        {self.description}
        {self.message}
        '''
        else:
            return 'Неизвестная ошибка!'


class MessageError(BaseException):
    """Custom message error."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Ошибка при отправке сообщения:'
        super().__init__(message=self.message, description=self.description)


class DateTimeError(BaseException):
    """Formatting date to unix error."""

    def __init__(self, message) -> None:
        self.message = message
        self.description = 'Не удалось обработать дату:'
        super().__init__(message=self.message, description=self.description)


class ResponseStatusError(BaseException):
    """Custom response status error."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Ошибка при обращении к серверу:'
        super().__init__(message=self.message, description=self.description)


class ResponseError(BaseException):
    """Custom response error."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Ошибка при обращении к API:'
        super().__init__(message=self.message, description=self.description)


class MainFuncError(BaseException):
    """Custom main-logic error."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Ошибка исполнения основной логики:'
        super().__init__(message=self.message, description=self.description)


class TokenNotFoundError(BaseException):
    """Custom token not found error."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Не найден токен:'
        super().__init__(message=self.message, description=self.description)


class ResponseWrongTypeError(BaseException):
    """Raises if response return not json-format answer."""

    def __init__(self, message) -> None:
        """Initializing custom token-error class."""
        self.message = message
        self.description = 'Неверный тип ответа от сервера:'
        super().__init__(message=self.message, description=self.description)
