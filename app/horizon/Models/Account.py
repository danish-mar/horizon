class Account:
    """
    Initializes An Account  from the database


    :param account_number: int - Account Number
    :param balance: int - Account Balance
    :param account_holder: User - The Account Holder
    :param is_active: boolean - is the Account Active
    """

    def __init__(self, account_number, balance, account_holder, is_active):
        self.account_number = None
        self.balance = 0
        self.account_holder = None
        self.is_active = False

    def get_account_number(self):
        return self.account_number

    def get_balance(self):
        return self.balance

    def get_account_holder(self):
        return self.account_holder

    def get_is_active(self):
        return self.is_active

    def initialize_account(self):
        self.account_number = None
        self.balance = 0
        self.account_holder = None
        self.is_active = False