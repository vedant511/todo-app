import pymongo
from pymongo import MongoClient
import config as cfg


class Database(object):
    DATABASE = None
    URI = cfg.DATABASE_URI

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI)
        Database.DATABASE = client['HomeMate_db']

    @staticmethod
    def insert_one(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def insert_many(collection, data_list):
        Database.DATABASE[collection].insert_many(data_list)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_many(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def delete_one(collection, query):
        result = Database.DATABASE[collection].delete_one(query)
        return result.deleted_count

    @staticmethod
    def delete_many(collection, query):
        result = Database.DATABASE[collection].delete_many(query)
        return result.deleted_count

    @staticmethod
    def create_index(collection, field, unique=True):
        Database.DATABASE[collection].create_index([field, pymongo.ASCENDING], unique)

    @staticmethod
    def index_info(collection):
        return sorted(list(Database.DATABASE[collection].index_information()))
