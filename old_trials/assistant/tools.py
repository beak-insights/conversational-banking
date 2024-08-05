from typing import Optional
import json
from datetime import datetime, timedelta
from dateutil.parser import parse

from langchain_core.tools import tool

from banking import BeakBank
from utils import class_to_dict


@tool
def lc_balance(user_id: str, account_type: str) -> str:
    """Balance checking only - his tool does not support withdrawals, deposits, sending, transfers, or other transactions.
    "Use this function to get the current account balance from the bank account manager.

    Args:
        user_id (str): The user ID associated with the account. Required
        account_type (str): The account type associated with the account. Required

    Returns:
        str: JSON: The current account balance in the account
    """

    if not user_id or not account_type:
        raise ValueError("User ID and account type are required")

    beak_bank = BeakBank().contextualise(user_id, None)
    balance = beak_bank.get_account_balance(account_type)

    return json.dumps({
        "account_type": account_type,
        "balance": balance
    })

@tool
def lc_deposit(user_id: str, account_type: str, amount: int) -> str:
    """Deposity only tool - Use this function to deposit money into an account. 

    Args:
        user_id (str): The user ID associated with the account. Required
        account_type (str): The account type associated with the account. Required
        amount (int): The amount to be deposited into the account. Required

    Returns:
        str: JSON The deposit status and corresponding transaction
    """

    if not user_id or not account_type or not amount:
        raise ValueError("User ID and account type and amount are all required")

    beak_bank = BeakBank().contextualise(user_id, None)
    account, transaction = beak_bank.deposit(account_type, amount)

    return json.dumps({
        "account_type": account_type,
        "success": account is not None,
        "transaction": class_to_dict(transaction)
    })

@tool
def lc_withdraw(user_id: str, account_type: str, amount: int) -> str:
    """Withdrawal only tool - Use this function to withdraw money from an account. 

    Args:
        user_id (str): The user ID associated with the account. Required
        account_type (str): The account type associated with the account. Required
        amount (int): The amount to be withdrawn from the account. Required

    Returns:
        str: JSON The withdrawal status and corresponding transaction
    """

    if not user_id or not account_type or not amount:
        raise ValueError("User ID and account type and amount are all required")

    beak_bank = BeakBank().contextualise(user_id, None)
    success, transaction = beak_bank.withdraw(account_type, amount)

    return json.dumps({
        "account_type": account_type,
        "success": success,
        "transaction": class_to_dict(transaction)
    })

@tool
def lc_internal_transfer(user_id: str, from_account_type: str, to_account_type: str, amount: int) -> str:
    """Internal (Transfer/sending) only tool - Use this function to transfer money between users own accounts only. 

    Args:
        user_id (str): The user ID associated with the account. Required
        from_account_type (str): The account type associated to withdraw from. Required
        to_account_type (str): The account type associated to transfer into. Required
        amount (int): The amount to be trabsfered from the account. Required

    Returns:
        str: JSON The transfer status and corresponding transaction
    """

    if not user_id or not from_account_type or not to_account_type or not amount:
        raise ValueError("User ID and from and to account types and amount are all required")

    beak_bank = BeakBank().contextualise(user_id, None)
    fr_acc, rf_tras, to_acc, to_trans = beak_bank.internal_transfer(from_account_type, to_account_type, amount)

    return json.dumps({
        "from_account_type": from_account_type,
        "to_account_type": to_account_type,
        "success": (fr_acc is not None) and (to_acc is not None),
        "transaction_from": class_to_dict(rf_tras),
        "transaction_to": class_to_dict(to_trans)
    })

@tool
def lc_external_transfer(user_id: str, from_account_type: str, beneficiary, amount: int) -> str:
    """External (Transfer/sending) only tool - Use this function to transfer money between users beneficiary or given account number. 

    Args:
        user_id (str): The user ID associated with the account. Required
        from_account_type (str): The account type associated to withdraw from. Required
        beneficiary (str): The beneficiary name or account number associated to transfer into. Required
        amount (float): The amount to be trabsfered from the account. Required

    Returns:
        str: JSON The transfer status and corresponding transaction
    """

    if not user_id or not from_account_type or not amount or not beneficiary:
        raise ValueError("User ID and from_account_type account types, beneficiary and amount are all required")

    beak_bank = BeakBank().contextualise(user_id, None)
    fr_acc, rf_tras, to_acc, to_trans = beak_bank.external_transfer(from_account_type, beneficiary, amount)

    return json.dumps({
        "from_account_type": from_account_type,
        "beneficiary":  beneficiary,
        "success": (fr_acc is not None) and (to_acc is not None),
        "transaction_from": class_to_dict(rf_tras),
        "transaction_to": class_to_dict(to_trans)
    })

def get_dates_last_n_days(n: int):
    """
    Use this function to get start date and end date given the last N days.
    
    Args:
        n: Number of days ago from today. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    start_date = datetime.now() - timedelta(days=int(n))
    end_date = datetime.now()
    return json.dumps({
        "start_date": start_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": end_date.strftime("%d-%m-%Y %H:%M:%S")
    })

def get_dates_last_n_hours(n: int):
    """
    Use this function to get start date and end date given the last N hours.
    
    Args:
        n: Number of hours that have passed from now. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    start_date = datetime.now() - timedelta(hours=int(n))
    end_date = datetime.now()
    return json.dumps({
        "start_date": start_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": end_date.strftime("%d-%m-%Y %H:%M:%S")
    })


def get_dates_from_to(start_date, end_date):
    """
    Use this function to get start date and end date as datetime objects given string start date and end date.
    
    Args:
        start_date: Start date as a string in "DD-MM-YYYY" format. Required
        end_date: Start date as a string in "DD-MM-YYYY" format. Required
        
    Return: 
        str: JSON with start_date and end_date range.
    """
    s_date = datetime.strptime(start_date, "%d-%m-%Y")
    e_date = datetime.strptime(end_date, "%d-%m-%Y")
    return  json.dumps({
        "start_date": s_date.strftime("%d-%m-%Y %H:%M:%S"),
        "end_date": e_date.strftime("%d-%m-%Y %H:%M:%S")
    })

@tool
def lc_statement(user_id: str, account_type: str, n_days_ago: Optional[int] = None, n_hours_ago: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
    """Use this function to get the bank statement to reflect user activity on their account.

    Args:
        user_id (str): The user ID associated with the account. Required
        account_type (str): The account type associated with the account. Required
        n_days_ago (Optional[int]): The number of days ago. Optional
        n_hours_ago (Optional[int]): The number of hours ago. Optional
        start_date (Optional[str]): The start date for the historical transactions. Optional
        end_date (Optional[str]): The End date for the historical transactions. Optional

    Returns:
        str: JSON: The bank statement
    """
    if not user_id or not account_type:
        raise ValueError("User ID and account type are required")

    if n_days_ago:
        dates = get_dates_last_n_days(n_days_ago)
    elif n_hours_ago:
        dates = get_dates_last_n_hours(n_hours_ago)
    elif start_date and end_date:
        dates = get_dates_from_to(start_date, end_date)
    else:
        dates = None
        
    if dates:
        dates = json.loads(dates)
    else:
      dates = {
            "start_date": (datetime.now() - timedelta(days=30)).strftime("%d-%m-%Y %H:%M:%S"),
            "end_date": None
        }

    # Fetch top story IDs
    beak_bank = BeakBank().contextualise(user_id, None)
    b_statement = beak_bank.get_bank_statement(
        account_type, 
        parse(dates.get("start_date"), dayfirst=True) if dates.get("start_date") else None, 
        parse(dates.get("end_date"), dayfirst=True) if dates.get("end_date") else None
    )
    return json.dumps({
        "account_type": account_type,
        "statement": class_to_dict(b_statement, 5)
    })
