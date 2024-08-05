from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

UtilityQuery = Query()
    

@dataclass
class UtilityBill:
    bill_id: str
    user_id: str
    account_id: str
    bill_type: str
    amount: str


class UtilityBillManager: 
    def get_one(self, bill_id):
        bill = db_manager.read(COLLECTIONS.BILLS, UtilityQuery.bill_id == bill_id)
        return UtilityBill(**bill[0]) if bill else None
   
    def get_all(self, user_id, account_id):
        bills = set(db_manager.read(COLLECTIONS.BILLS, (UtilityQuery.user_id == user_id) | (UtilityQuery.account_id == account_id)))
        return [UtilityBill(**bill) for bill in bills]
    
    def add_bill(self, user_id, account_id, bill_type, amount):
        bill = UtilityBill(user_id, account_id, bill_type, amount)
        bill = db_manager.create(COLLECTIONS.BILLS, bill.__dict__)
        return UtilityBill(**bill)
