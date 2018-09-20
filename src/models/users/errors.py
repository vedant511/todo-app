__author__ = 'Vedant Sharma'


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class UsernameTakenError(UserError):
    pass


class InvalidEmailError(UserError):
    pass


class InvalidPasswordError(UserError):
    pass


class EmptyFieldsError(UserError):
    pass
