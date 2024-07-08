class Transaction:

    def __init__(self, transaction_id, transaction_type, amount, from_account, to_account, description):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.description = description


    def get_transaction_id(self):
        return self.transaction_id

    def get_transaction_type(self):
        return self.transaction_type

    def get_amount(self):
        return self.amount

    def get_from_account(self):
        return self.from_account

    def get_to_account(self):
        return self.to_account

    def get_description(self):
        return self.description