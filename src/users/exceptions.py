class IncorrectPasswordError(Exception):
    """Raised when user enters incorrect password."""


class SamePasswordError(Exception):
    """Raised when user enters same password like old one."""


class RegisterException(Exception):
    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason


class UpdateUserException(Exception):
    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason


class ChangePasswordException(Exception):
    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason
