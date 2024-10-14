

class BankStatement:
    def __init__(self, account_type, start_date, end_date, start_balance, end_balance, transactions):
        self.account_type = account_type
        self.start_date = start_date
        self.end_date = end_date
        self.start_balance = start_balance
        self.end_balance = end_balance
        self.transactions = transactions

    def __str__(self):
        statement = f"Your {self.account_type} Statement\n"
        statement += f"Period: {self.start_date} - {self.end_date}\n"
        statement += f"Starting Balance: {self.start_balance}\n"
        statement += f"Ending Balance: {self.end_balance}\n"
        statement += "Transactions:\n"
        for transaction in self.transactions:
            statement += f"  {transaction}\n"
        return statement
    