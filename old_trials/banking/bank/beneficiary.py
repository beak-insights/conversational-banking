import uuid

from pydantic.dataclasses import dataclass
from tinydb import Query

from .db import COLLECTIONS, db_manager

BeneficiaryQuery = Query()


@dataclass
class Beneficiary:
    beneficiary_id: str
    name: str
    account_number: str
    user_id: str


class BeneficiaryManager:
    def get_all(self, user_id: str):
        if user_id:
            beneficiaries = db_manager.read(COLLECTIONS.BENEFICIARIES, BeneficiaryQuery.user_id == user_id)
        else:
            beneficiaries = db_manager.read(COLLECTIONS.BENEFICIARIES)
        return [Beneficiary(**benefactor) for benefactor in beneficiaries]
    
    def get_by_name(self, name: str):
        beneficiary = db_manager.read(COLLECTIONS.BENEFICIARIES, BeneficiaryQuery.name == name)
        return Beneficiary(**beneficiary[0]) if beneficiary else None
    
    def add_beneficiary(self, user_id, name, account_number):
        beneficiary = self.get_by_name(name)
        if beneficiary:
            raise Exception(f"Beneficiary with name {name} already exists")
        new_beneficiary = Beneficiary(uuid.uuid4().hex, name, account_number, user_id)
        beneficiary = db_manager.create(COLLECTIONS.BENEFICIARIES, new_beneficiary.__dict__)
        return Beneficiary(**beneficiary)
