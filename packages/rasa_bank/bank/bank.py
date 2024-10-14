
from .account import AccountManager
from .beneficiary import BeneficiaryManager
from .ledger import LedgerManager
from .statement import BankStatement
from .transaction import TransactionManager
from .user import UserManager
from .utility import UtilityBillManager
from ..seeder import seed_for_user

class BeakBank:
    """MyBeakBank class to manage all banking operations."""
    # user context
    user_id = None

    def __init__(self):
        # managers
        self.user_manager = UserManager()
        self.account_manager = AccountManager()
        self.transaction_manager = TransactionManager()
        self.ledger_manager = LedgerManager()
        self.bill_manager = UtilityBillManager()
        self.beneficiary_manager = BeneficiaryManager()

    def contextualise(self, user_id):
        """Set the user context for the bank.
        This will simplify the API by not requiring the user_id to be passed in every method call e.t.c
        """
        self.user_id = user_id
        return self
    
    def init(self):
        # check if user exists
        user = self.user_manager.get_one(self, self.user_id)
        if not user:
            raise Exception("Either you dont have an account with the bank or you have not synchronised this bot.")
        return self

    def create_user(self, user_id, name, email, password):
        user_id = user_id if user_id else self.user_id
        user = self.user_manager.get_or_create(user_id, name, email, password)
        return user

    def create_account(self, user_id, account_number, account_type):
        user_id = user_id if user_id else self.user_id
        account = self.account_manager.get_or_create(user_id, account_number, account_type)
        return account
    
    def add_beneficiary(self, name, account_number):
        beneficiary = self.beneficiary_manager.add_beneficiary(self.user_id, name, account_number)
        return beneficiary

    def deposit(self, account_type, amount):
        account = self.account_manager.get_one_by_type(self.user_id, account_type)
        pre_balance = account.balance
        account = self.account_manager.deposit(account.account_number, amount)
        transaction = None
        if account:
            transaction = self.transaction_manager.add_transaction(account.account_id, "deposit", amount, pre_balance, account.balance)
            self.ledger_manager.add_entry(account.account_id, transaction.transaction_id, "debit", amount)
        return account, transaction

    def withdraw(self, account_type, amount):
        account = self.account_manager.get_one_by_type(self.user_id, account_type)
        pre_balance = account.balance
        account = self.account_manager.withdraw(account.account_number, amount)
        transaction = None
        if account:
            transaction = self.transaction_manager.add_transaction(account.account_id, "withdrawal", amount, pre_balance, account.balance)
            self.ledger_manager.add_entry(account.account_id, transaction.transaction_id, "credit", amount)
        return account, transaction

    def internal_transfer(self, from_account_type, to_account_type, amount):
        from_account = self.account_manager.get_one_by_type(self.user_id, from_account_type)
        to_account = self.account_manager.get_one_by_type(self.user_id, to_account_type)
        if not to_account:
            raise Exception(f"Beneficiary account ({from_account_type}) not found.")
        if not from_account:
            raise Exception(f"Desitnation account ({to_account_type}) not found.")
        return self._transfer(from_account, to_account, amount)

    def external_transfer(self, from_account_type, beneficiary, amount):
        from_account = self.account_manager.get_one_by_type(self.user_id, from_account_type)
        to_account = self._resolve_beneficiary(beneficiary)
        if not to_account:
            raise Exception(f"Beneficiary account ({beneficiary}) not found.")
        if not from_account:
            raise Exception(f"Source account ({from_account_type}) not found.")
        return self._transfer(from_account, to_account, amount)
    
    def _resolve_beneficiary(self, beneficiary):
        to_account = self.account_manager.get_one_by_number(beneficiary)
        if not to_account:
            _beneficiary = self.beneficiary_manager.get_by_name(beneficiary)
            if not _beneficiary:
                raise Exception(f"Incorrect Beneficiary Name.")
            to_account = self.account_manager.get_one_by_number(_beneficiary.account_number)
        return to_account

    def _transfer(self, from_acc, to_acc, amount):
        from_account = self.account_manager.withdraw(from_acc.account_number, amount)
        to_account = self.account_manager.deposit(to_acc.account_number, amount)

        if not from_account or not to_account:
            raise Exception("Transfer failed. Please contact the bank.")
        transaction_from = self.transaction_manager.add_transaction(from_account.account_id, "transfer out", amount, from_acc.balance, from_account.balance)
        self.ledger_manager.add_entry(from_account.account_id, transaction_from.transaction_id, "credit", amount)
        transaction_to = self.transaction_manager.add_transaction(to_account.account_id, "transfer in", amount, to_acc.balance, to_account.balance)
        self.ledger_manager.add_entry(to_account.account_id, transaction_to.transaction_id, "debit", amount)
        return from_account, transaction_from, to_account, transaction_to

    def pay_bill(self, account_type, bill_type, amount):
        account = self.account_manager.get_one_by_type(self.user_id, account_type)
        pre_balance = account.balance
        account = self.account_manager.withdraw(account_number=account.account_number, amount=amount)
        if not account:
            raise Exception("Bill payment failed. Please contact the bank.")
        self.bill_manager.add_bill(self.user_id, account.account_id, bill_type, amount)
        transaction = self.transaction_manager.add_transaction(account.account_id, "bill", amount, pre_balance, account.balance)
        self.ledger_manager.add_entry(account.account_id, transaction.transaction_id, "credit", amount)
        return account, transaction
        
    def get_account_balance(self, account_type):
        return self.account_manager.get_account_balance(self.user_id, account_type)
    
    def get_accounts(self):
        return self.account_manager.get_all(self.user_id)
    
    def get_beneficiaries(self):
        return self.beneficiary_manager.get_all(self.user_id)

    def get_transaction_history(self, account_type, start_date, end_date):
        print(self.user_id, account_type, start_date, end_date)
        account = self.account_manager.get_one_by_type(self.user_id, account_type)
        print(account.__dict__)
        return self.transaction_manager.get_all(account.account_id, start_date, end_date)

    def get_ledger_entries(self, account_type):
        account = self.account_manager.get_one_by_type(self.user_id, account_type)
        return self.ledger_manager.get_all(account.account_id)

    def get_bank_statement(self, account_type, start_date, end_date):
        transactions = self.get_transaction_history(account_type, start_date, end_date)
        if not transactions:
            return f"The {account_type} account has no transactions found for the specified period: start_date: {start_date}, end_date: {end_date}"
        
        bank_statement = BankStatement(
            account_type=account_type,
            start_date=start_date,
            end_date=end_date,
            start_balance=transactions[0].pre_balance,
            end_balance=transactions[-1].post_balance,
            transactions=transactions
        )
        return bank_statement
    

# initialise the bank instance a.k.a singleton
beak_bank = BeakBank()



