from pymongo import MongoClient
import instance.config as cfg

client = MongoClient(cfg.DATABASE_URI)

print(client.dbs)
