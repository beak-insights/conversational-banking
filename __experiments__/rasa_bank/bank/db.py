import os

from tinydb import TinyDB

db_dir = os.path.join(os.path.dirname(__file__), "..", "db")



class COLLECTIONS:
    USERS = "users"
    ACCOUNTS = "accounts"
    TRANSACTIONS = "transactions"
    LEDGER = "ledger"
    BILLS = "bills"
    BENEFICIARIES = "beneficiaries"


class BankDBManager:
    def __init__(self, db_path="bank-db.json"):
        self.db = TinyDB(F"{db_dir}/{db_path}")

    def create(self, table_name, data):
        table = self.db.table(table_name)
        id = table.insert(data)
        return table.get(doc_id=id)

    def read(self, table_name, query=None):
        table = self.db.table(table_name)
        if query:
            return table.search(query)
        else:
            return table.all()

    def update(self, table_name, query, updates):
        table = self.db.table(table_name)
        table.update(updates, query)
        return table.search(query)

    def delete(self, table_name, query):
        table = self.db.table(table_name)
        table.remove(query)

    def close(self):
        self.db.close()


db_manager = BankDBManager()