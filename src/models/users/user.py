from src.common.database import Database
import src.models.users.errors as UserErrors
from flask import session
from flask_bcrypt import Bcrypt
import re


class User(object):

    bcrypt = Bcrypt()

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
            raise UserErrors.EmptyFieldsError('All fields are required')

        if len(pwd) not in range(6, 17):
            raise UserErrors.InvalidPasswordError('Password must be 6-16 characters long')

        if not re.match(r'^[\w-]+@([\w-]+\.)+[\w]+$', email):
            raise UserErrors.InvalidEmailError('Email address you entered is invalid')

        if cls.get_by_mail(email):
            raise UserErrors.UserAlreadyRegisteredError('This Email is already registered, please Login instead')

        if cls.get_by_unm(username):
            raise UserErrors.UsernameTakenError('This Username is already taken, please select a different one')

        hashed_pwd = User.bcrypt.generate_password_hash(pwd).decode('utf-8')

        new_user = cls(name, email, hashed_pwd, username)
        Database.insert('users', new_user.json())
        session['email'] = email
        return True

    @classmethod
    def login(cls, identifier, password):
        if cls.get_by_mail(identifier) is not None:
            user = cls.get_by_mail(identifier)
            if User.bcrypt.check_password_hash(user.pwd, password):
                session['email'] = user.email
                return True
            else:
                raise UserErrors.InvalidPasswordError('Username or Password is incorrect, please try again')

        elif cls.get_by_unm(identifier) is not None:
            user = cls.get_by_unm(identifier)
            if User.bcrypt.check_password_hash(user.pwd, password):
                session['email'] = user.email
                return True
            else:
                raise UserErrors.InvalidPasswordError('Username or Password is incorrect, please try again')

        else:
            raise UserErrors.UserNotExistsError('This User does not exist, please register to continue')

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
