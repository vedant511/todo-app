from app.database import Database


class User(object):

    def __init__(self, name, email, pwd, username):
        self.name = name
        self.email = email
        self.pwd = pwd
        self.username = username

    @classmethod
    def get_by_mail(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None or data is False:
            return cls(**data)

    @classmethod
    def get_by_unm(cls, username):
        data = Database.find_one("users", {"username": username})
        if data is not None or data is False:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None or data is False:
            return cls(**data)

    @classmethod
    def register(cls, name, email, pwd, username):
        if cls.get_by_mail(email) is not None or cls.get_by_unm(username) is not None:
            return False

        else:
            new_user = cls(name, email, pwd, username)
            Database.insert('users', new_user.json())
            return True

    @classmethod
    def login(cls, identifier, password):
        if cls.get_by_mail(identifier) is not None:
            user = cls.get_by_mail(identifier)
            return user.pwd == password

        elif cls.get_by_unm(identifier) is not None:
            user = cls.get_by_unm(identifier)
            return user.pwd == password

        else:
            # User does not exist
            return False

    def json(self):
        return{
            "name": self.name,
            "email": self.email,
            "pwd": self.pwd,
            "username": self.username,
        }
