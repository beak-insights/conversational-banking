import uuid

from datetime import datetime
from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

TransactionQuery = Query()
    

@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    transaction_type: str
    amount: float
    pre_balance: float
    post_balance: float
    transaction_date: datetime


def _transaction(transaction: dict) -> Transaction:
    return Transaction(**{
        **transaction,
        "transaction_date": datetime.strptime(transaction["transaction_date"], "%Y-%m-%d %H:%M:%S")
    })

class TransactionManager:
    def get_one(self, transaction_id):
        transaction = db_manager.read(COLLECTIONS.TRANSACTIONS, TransactionQuery.transaction_id == transaction_id)
        return _transaction(transaction[0]) if transaction else None

    def get_all(self, account_id, gt_date, lt_date):
        if not account_id:
            transactions = db_manager.read(COLLECTIONS.TRANSACTIONS)
        else:
            transactions = db_manager.read(COLLECTIONS.TRANSACTIONS, TransactionQuery.account_id == account_id)
        transactions = [_transaction(transaction) for transaction in transactions]
        if lt_date:
            transactions = filter(lambda transaction: transaction.transaction_date <= lt_date, transactions)
        if gt_date:
            transactions = filter(lambda transaction: transaction.transaction_date >= gt_date, transactions)
        return list(transactions)

    def add_transaction(self, account_id, transaction_type, amount, pre_balance, post_balance):
        new_transaction = Transaction(
            uuid.uuid4().hex, account_id, transaction_type, amount, 
            pre_balance, post_balance, datetime.now()
        )
        transaction = db_manager.create(COLLECTIONS.TRANSACTIONS, {
            **new_transaction.__dict__,
            "transaction_date": new_transaction.transaction_date.strftime("%Y-%m-%d %H:%M:%S")
        })
        return _transaction(transaction)


