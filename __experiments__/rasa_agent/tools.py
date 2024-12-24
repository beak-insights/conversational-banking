import os
from typing import Optional

from httpx import AsyncClient
from langchain_core.tools import tool

BANK_API = os.getenv('BANK_API')

async def bank_request(url, data):
    print("bank_request", url, data)
    async with AsyncClient(base_url=BANK_API) as client:
        try:
            response = await client.post(url, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except Exception as err:
            print(f"Other error occurred: {str(err)}")
            return {"error": f"An unexpected error occurred: {str(err)}"}


@tool
async def lc_balance(user_id: str, account_type: str) -> str:
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
    print("user_id", user_id, "account_type", account_type)
    return await bank_request("/balance", {"user_id": user_id, "account_type": account_type})

@tool
async def lc_deposit(user_id: str, account_type: str, amount: int) -> str:
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
    return await bank_request("/deposit", {"user_id": user_id, "account_type": account_type, "amount": amount})

@tool
async def lc_withdraw(user_id: str, account_type: str, amount: int) -> str:
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
    return await bank_request("/withdraw", {"user_id": user_id, "account_type": account_type, "amount": amount})

@tool
async def lc_internal_transfer(user_id: str, from_account_type: str, to_account_type: str, amount: int) -> str:
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
    return await bank_request("/internal-transfer", {
        "user_id": user_id, 
        "from_account_type": from_account_type, 
        "to_account_type": to_account_type,
        "amount": amount
    })


@tool
async def lc_external_transfer(user_id: str, from_account_type: str, beneficiary, amount: int) -> str:
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
    return await bank_request("/external-transfer", {
        "user_id": user_id, 
        "from_account_type": from_account_type, 
        "beneficiary": beneficiary,
        "amount": amount
    })

@tool
async def lc_statement(user_id: str, account_type: str, n_days_ago: Optional[int] = None, n_hours_ago: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
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

    if not n_days_ago and not n_hours_ago and not start_date and not end_date:
        raise ValueError("At least one of n_days_ago, n_hours_ago, start_date or end_date is required")
    
    return await bank_request("/bank-statement", {
        "user_id": user_id, 
        "account_type": account_type, 
        "n_days_ago": n_days_ago, 
        "n_hours_ago": n_hours_ago, 
        "start_date": start_date, 
        "end_date": end_date
    })
