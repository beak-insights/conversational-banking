import os
from aiotinydb import AIOTinyDB

db_dir = os.path.join(os.path.dirname(__file__), ".", "db")


class COLLECTIONS:
    USERS = "users"
    ACTIVITIES = "activities"


class AIDBManager:
    def __init__(self, db_path="ai-db.json"):
        self.db = AIOTinyDB(F"{db_dir}/{db_path}")

    async def create(self, table_name, data):
        async with self.db as db:
            table = db.table(table_name)
            id = table.insert(data)
            return table.get(doc_id=id)

    async def read(self, table_name, query=None):
        async with self.db as db:
            table = db.table(table_name)
            if query:
                return table.search(query)
            else:
                return table.all()

    async def update(self, table_name, query, updates):
        async with self.db as db:
            table = db.table(table_name)
            table.update(updates, query)
            return table.search(query)

    async def delete(self, table_name, query):
        async with self.db as db:
            table = db.table(table_name)
            table.remove(query)

    async def close(self):
        async with self.db as db:
            db.close()


db_manager = AIDBManager()
