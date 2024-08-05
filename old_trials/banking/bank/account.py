import uuid

from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

AccountQuery = Query()


@dataclass
class Account:
    account_id: str
    user_id: str
    account_number: str
    account_balance: float
    account_type: str

    @property
    def balance(self):
        return self.account_balance


class AccountManager:
    def get_all(self, user_id: str):
        accounts = db_manager.read(COLLECTIONS.ACCOUNTS, AccountQuery.user_id == user_id)
        return [Account(**account) for account in accounts]
    
    def get_one_by_type(self, user_id, account_type: str):
        account = db_manager.read(COLLECTIONS.ACCOUNTS, AccountQuery.fragment({'user_id': user_id, 'account_type': account_type}))
        return Account(**account[0]) if account else None
    
    def get_one_by_number(self, account_number: str):
        account = db_manager.read(COLLECTIONS.ACCOUNTS, AccountQuery.account_number == account_number)
        return Account(**account[0]) if account else None
        
    def get_account_balance(self, user_id, account_type: str):
        account = self.get_one_by_type(user_id, account_type)
        if not account:
            raise Exception(f"Cannot retrieve balance for a non existset Account of type ({account_type})")
        return account.balance
    
    def get_or_create(self, user_id, account_number, account_type):
        account = self.get_one_by_number(account_number)
        if account:
            if not account.user_id == user_id:
                raise Exception(f"Account with number {account_number} already exists for another user")
            raise Exception(f"{account_type} Account with number {account_number} already exists for this user")

        new_account = Account(uuid.uuid4().hex, user_id, account_number, float(0.0), account_type)
        account = db_manager.create(COLLECTIONS.ACCOUNTS, new_account.__dict__)
        return Account(**account)

    def deposit(self, account_number, amount):
        account = self.get_one_by_number(account_number)
        if not account:
            raise Exception(f"Account with number {account_number} does not exist")
        new_labance = account.balance + amount
        account = db_manager.update(COLLECTIONS.ACCOUNTS, AccountQuery.account_number == account_number, {'account_balance': new_labance})
        return Account(**account[0])

    def withdraw(self, account_number, amount):
        account = self.get_one_by_number(account_number)
        if not account:
            raise Exception(f"Account with number {account_number} does not exist")
        if account.balance < amount:
            raise Exception(f"Insufficient funds. Current balance is {account.balance}")
        new_labance = account.balance - amount
        account = db_manager.update(COLLECTIONS.ACCOUNTS, AccountQuery.account_number == account_number, {'account_balance': new_labance})
        return Account(**account[0])
