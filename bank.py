# bank.py
class Bank:
    def __init__(self):
        self.accounts = {}  # Dictionary to store account objects

    def add_account(self, accno, balance=0.0):
        # Create a new account and add it to the dictionary
        self.accounts[accno] = {'balance': balance}
        return f"Account {accno} created with balance {balance}"

    def deposit(self, accno, amount):
        if accno in self.accounts:
            self.accounts[accno]['balance'] += amount
            return f"Deposited {amount} into account {accno}. New balance: {self.accounts[accno]['balance']}"
        else:
            return f"Account number {accno} not found."

    def withdraw(self, accno, amount):
        if accno in self.accounts:
            if self.accounts[accno]['balance'] >= amount:
                self.accounts[accno]['balance'] -= amount
                return f"Withdrew {amount} from account {accno}. New balance: {self.accounts[accno]['balance']}"
            else:
                return f"Insufficient funds in account {accno}."
        else:
            return f"Account number {accno} not found."

    def get_balance(self, accno):
        if accno in self.accounts:
            return self.accounts[accno]['balance']
        else:
            return f"Account number {accno} not found."
