import hashlib
from pprint import pprint

class Transaction:
    def __init__(self, transaction_id, account_id, amount, transaction_type, description, created_at, previous_hash, from_account, to_account, platform):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.created_at = created_at
        self.previous_hash = previous_hash
        self.from_account = from_account
        self.to_account = to_account
        self.platform = platform

    # Copy constructor to initialize from a database result set
    @classmethod
    def from_db_result(cls, db_result):
        return cls(
            transaction_id=db_result[0],
            account_id=db_result[1],
            amount=db_result[2],
            transaction_type=db_result[3],
            description=db_result[4],
            created_at=db_result[5],
            previous_hash=db_result[6],
            from_account=db_result[7],
            to_account=db_result[8],
            platform=db_result[9]
        )

    def calculate_hash(self):
        hash_string = f"{self.transaction_id}{self.account_id}{self.amount}{self.transaction_type}{self.description}{self.created_at}{self.previous_hash}{self.from_account}{self.to_account}{self.platform}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def __str__(self):
        return pprint(vars(self))