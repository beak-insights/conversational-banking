import uuid
import random

from faker import Faker

from . import BeakBank

fake = Faker()


def get_user_context(user_id):
    bank = BeakBank().contextualise(user_id)
    user_accounts = bank.account_manager.get_all(user_id)
    beneficiaries = bank.beneficiary_manager.get_all(user_id)
    return {
        "username": bank.user_manager.get_one(user_id).name,
        "context": f"""
        1. User has {len(user_accounts)} accounts namely: {", ".join([acc.account_type for acc in user_accounts])}
        2. User has {len(beneficiaries)} beneficiaries namely: {", ".join([b.name for b in beneficiaries])}
        """
    }

def seed_for_user(user_id: str, full_name: str | None = None) -> str:
    """Initialize accounts for a user."""
    bank = BeakBank().contextualise(user_id)

    if not user_id:
        raise ValueError("User ID is required for seeding")
    
    if not bank:
        raise ValueError("Contextual Bank not initialized.")
    
    user_id = str(user_id)
    # 1. create user account

    if bank.user_manager.get_one(user_id):
        return get_user_context(user_id)
    
    bank.create_user(user_id, full_name, None, None)

    # 2. create accounts [savings, current, fixed, spending]
    user_accounts = [
        bank.create_account(user_id, fake.aba(), bac) 
        for bac in ["savings", "current", "fixed", "spending"]
    ]

    # 3. deposit initial big amount into current account
    for amount in [random.randint(300,1000) for _ in range(1,5)]:
        bank.deposit("current", amount)

    # 4, Create  from 1 to 4 accounts as beneficiaries for the user
    user_beneficiaries = [
        bank.create_user(uuid.uuid4().hex, fake.name().replace(" ", ""), None, None)
        for _ in range(0,3)
    ]
    beneficiaries = []
    for user_ben in user_beneficiaries:
        beneficiary_account = bank.create_account(user_ben.user_id, fake.aba(), "current")
        beneficiary = bank.add_beneficiary(user_ben.name, beneficiary_account.account_number)
        beneficiaries.append(beneficiary)
    # 5. return seeded user context for llm use
    return get_user_context(user_id)


