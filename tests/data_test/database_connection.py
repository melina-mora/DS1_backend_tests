import pymongo


class DatabaseConn:
    def __init__(self, db=None, coll=None):
        self._conn = pymongo.MongoClient("mongodb://localhost:27017/")  # Connection to local MongoDB
        self.db = self._conn[db] if db else None  # Connection to database
        self.coll = self.db[coll] if coll else None  # Connection to collection/table
