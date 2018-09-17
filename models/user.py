from app.database import Database
from flask import session
import re


class User(object):

    def __init__(self, name, email, pwd, username, _id=None, isAdmin=0):
        self.name = name
        self.email = email
        self.pwd = pwd
        self.username = username
        self._id = _id
        self.isAdmin = isAdmin

    @classmethod
    def get_by_mail(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_unm(cls, username):
        data = Database.find_one("users", {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, name, email, pwd, username):
        if name == "" or email == "" or pwd == "" or username == "":
            return "All fields are required"

        if len(pwd) not in range(6, 17):
            return 'Password must be 6-16 characters long'

        if not re.match(r'(.)+(@)(.)+(\.)(.)+', email):
            return 'Email Address you entered is invalid'

        if cls.get_by_mail(email):
            return "This Email is already registered, please Login to continue"

        if cls.get_by_unm(username):
            return "This Username is already taken, please select a different one"

        new_user = cls(name, email, pwd, username)
        Database.insert('users', new_user.json())
        session['email'] = email
        return "Registered"

    @classmethod
    def login(cls, identifier, password):
        if cls.get_by_mail(identifier) is not None:
            user = cls.get_by_mail(identifier)
            if user.pwd == password:
                session['email'] = user.email
                return True

        elif cls.get_by_unm(identifier) is not None:
            user = cls.get_by_unm(identifier)
            if user.pwd == password:
                session['email'] = user.email
                return True

        else:
            # User does not exist
            return False

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return{
            "name": self.name,
            "email": self.email,
            "pwd": self.pwd,
            "username": self.username,
            "isAdmin": self.isAdmin
        }
