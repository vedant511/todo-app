from src.common.database import Database
import re
import datetime


class Task(object):

    def __init__(self, user_id, title, description, time_due, priority, time_remind, reminder_freq, group):
        self._id = None
        self.user_id = user_id
        self.title = title
        self.description = description
        self.timeAdded = datetime.datetime.utcnow()
        self.timeDue = time_due
        self.priority = priority
        self.timeRemind = time_remind
        self.reminderFreq = reminder_freq
        self.group = group
        self.numReminded = 0
        self.isComplete = 0
        self.isOverdue = 0

    @classmethod
    def create_task(cls, user_id, title, description, time_due, priority, time_remind, reminder_freq, group):
        ## Check if time_remind is < time_due
        new_task = cls(user_id, title, description, time_due, priority, time_remind, reminder_freq, group)
        Database.insert('tasks', new_task.json())
        return True

    @classmethod
    def get_by_task_id(cls, task_id):
        data = Database.find_one('tasks', {'_id': task_id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def get_by_user_id(user_id):
        data = list(Database.find_all('tasks', {'user_id': user_id}))
        return data

    @staticmethod
    def get_by_filter(filter_query, project_query):
        data = list(Database.find_all('tasks', filter_query, proj=project_query))
        return data

    @staticmethod
    def delete_single(task_id):
        return Database.delete_one('tasks', {'_id': task_id})

    @staticmethod
    def delete_multiple(del_query):
        return Database.delete_many('tasks', del_query)

    @staticmethod
    def edit_task(filter_query, edit_query):
        return Database.update_one('tasks', filter_query, edit_query)

    def json(self):
        return {
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'timeAdded': self.timeAdded,
            'timeDue': self.timeDue,
            'priority': self.priority,
            'timeRemind': self.timeRemind,
            'reminderFreq': self.reminderFreq,
            'group': self.group,
            'numReminded': self.numReminded,
            'isComplete': self.isComplete,
            'isOverdue': self.isOverdue,
        }
