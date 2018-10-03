__author__ = 'Vedant Sharma'


class TaskError(Exception):
    def __init__(self, message):
        self.message = message


class TaskNotExistsError(TaskError):
    pass


class EmptyFieldsError(TaskError):
    pass


class TimeFrameError(TaskError):
    pass
