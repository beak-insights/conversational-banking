import uuid

from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

LedgerQuery = Query()
    

@dataclass
class LedgerEntry:
    ledger_id: str
    account_id: str
    transaction_id: str
    debit_credit: str
    amount: float


class LedgerManager:
    def get_one(self, ledger_id):
        entry = db_manager.read(COLLECTIONS.LEDGER, LedgerQuery.ledger_id == ledger_id)
        return LedgerEntry(**entry[0]) if entry else None

    def get_all(self, account_id):
        entries = db_manager.read(COLLECTIONS.LEDGER, LedgerQuery.account_id == account_id)
        return [LedgerEntry(**entry) for entry in entries]
    
    def add_entry(self, account_id, transaction_id, debit_credit, amount):
        new_ledger_entry = LedgerEntry(uuid.uuid4().hex, account_id, transaction_id, debit_credit, amount)
        entry = db_manager.create(COLLECTIONS.LEDGER, new_ledger_entry.__dict__)
        return LedgerEntry(**entry)
