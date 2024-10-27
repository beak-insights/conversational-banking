import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, model_validator

from . import BeakBank
from .seeder import seed_for_user
from .utils import (
    get_dates_from_to, 
    get_dates_last_n_days, 
    get_dates_last_n_hours
)


app = FastAPI()


class BaseQuery(BaseModel):
    user_id: str
    
    
class ContextQuery(BaseQuery):
    full_name: Optional[str] = None


@app.post("/context")
def user_context(data: ContextQuery):
    print(f"Requesting context for {data.user_id}:{data.full_name}")
    ctx = seed_for_user(data.user_id, data.full_name)
    print(f"Context for {data.user_id} is {ctx}")   
    return {"content":  ctx}


class SeedRequest(BaseQuery):
    full_name: Optional[str] = None


@app.post("/seed")
def seed_user(data: SeedRequest):
    return {"content": seed_for_user(data.user_id, data.full_name) }


class BalanceRequest(BaseQuery):
    account_type: str


@app.post("/balance")
async def balance(data: BalanceRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    return {"content": beak_bank.get_account_balance(data.account_type)}


class AccountsRequest(BaseQuery):
    ...


@app.post("/accounts")
async def balance(data: AccountsRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    accounts = beak_bank.get_accounts()
    beneficiaries = beak_bank.get_beneficiaries()
    return {"content": {
        "accounts": [acc.account_type for acc in accounts],
        "beneficiaries": [ben.name for ben in beneficiaries]
    }}

class DepositRequest(BaseQuery):
    account_type: str
    amount: float

@app.post("/deposit")
async def deposit(data: DepositRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    account, transaction = beak_bank.deposit(data.account_type, data.amount)
    return {
        "new_balance": f"Increased from {transaction.pre_balance} to {transaction.post_balance}"
    }


class WithdrawalRequest(BaseQuery):
    account_type: str
    amount: float


@app.post("/withdraw")
async def withdraw(data: WithdrawalRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    try:
        account, transaction = beak_bank.withdraw(data.account_type, data.amount)
        return {
            "new_balance": f"Reduced from {transaction.pre_balance} to {transaction.post_balance}"
        }
    except Exception as e:
        return {"error": str(e)}


class InternalTransferRequest(BaseQuery):
    from_account_type: str
    to_account_type: str
    amount: float


@app.post("/internal-transfer")
async def internal_transfer(data: InternalTransferRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    try:
        fr_acc, fr_tras, to_acc, to_trans = beak_bank.internal_transfer(data.from_account_type, data.to_account_type, data.amount)
        return {
            "from_account_balance": f"Reduced from {fr_tras.pre_balance} to {fr_tras.post_balance}",
            "to_account_balance": f"Increased from {to_trans.pre_balance} to {to_trans.post_balance}",
        }
    except Exception as e:
        return {"error": str(e)}

class ExternalTransferRequest(BaseQuery):
    from_account_type: str
    beneficiary: str
    amount: float


@app.post("/external-transfer")
async def external_transfer(data: ExternalTransferRequest):
    beak_bank: BeakBank = BeakBank().contextualise(data.user_id)
    try:
        fr_acc, fr_tras, to_acc, to_trans = beak_bank.external_transfer(data.from_account_type, data.beneficiary, data.amount)
        return {
            "balance": f"Reduced from {fr_tras.pre_balance} to {fr_tras.post_balance}",
        }
    except Exception as e:
        return {"error": str(e)}


class BankStatementRequest(BaseQuery):
    account_type: str
    n_days_ago: Optional[int] = None, 
    n_hours_ago: Optional[int] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None

    @model_validator(mode='before')
    def check_optionals(cls, values):
        if not values.get('n_days_ago') and not values.get('n_hours_ago') and not values.get('start_date') and not values.get('end_date'):
            raise ValueError('either n_days_ago, n_hours_ago, start_date or end_date is required')
        return values


@app.post("/bank-statement")
async def bank_statement(data: BankStatementRequest):
    bank: BeakBank = BeakBank().contextualise(data.user_id)

    if data.n_days_ago:
        dates = get_dates_last_n_days(data.n_days_ago)
    elif data.n_hours_ago:
        dates = get_dates_last_n_hours(data.n_hours_ago)
    elif data.start_date and data.end_date:
        dates = get_dates_from_to(data.start_date, data.end_date)
    else:
        dates = None
        
    if dates:
        dates = json.loads(dates)
    else:
      dates = {
            "start_date": (datetime.now() - timedelta(days=30)).strftime("%d-%m-%Y %H:%M:%S"),
            "end_date": None
        }

    beak_bank:BeakBank = BeakBank().contextualise(data.user_id)
    b_statement = beak_bank.get_bank_statement(
        data.account_type, 
        parse(dates.get("start_date"), dayfirst=True) if dates.get("start_date") else None, 
        parse(dates.get("end_date"), dayfirst=True) if dates.get("end_date") else None
    )


    return { "statement": b_statement, 
            "example_format": """
                📄 **Bank Statement**
                **Account Holder:** John Doe
                **Account Number:** XXXX-XXXX-XXXX-1234
                **Statement Period:** 01 Jan 2024 - 31 Jan 2024

                **Opening Balance:** $1,200.00

                **Transactions:**
                1. 📅 **01 Jan 2024**
                - **Description:** Grocery Store
                - **Amount:** -$45.00
                - **Balance:** $1,155.00

                2. 📅 **05 Jan 2024**
                - **Description:** Salary
                - **Amount:** +$2,500.00
                - **Balance:** $3,655.00

                ...

                **Closing Balance:** $3,320.00
                """ 
            }
