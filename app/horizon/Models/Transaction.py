import hashlib
from pprint import pprint

class Transaction:
    def __init__(self, transaction_id, account_id, amount, transaction_type, description, created_at, previous_hash):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.created_at = created_at
        self.previous_hash = previous_hash

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
            previous_hash=db_result[6]
        )

    def calculate_hash(self):
        hash_string = f"{self.transaction_id}{self.account_id}{self.amount}{self.transaction_type}{self.description}{self.created_at}{self.previous_hash}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def __str__(self):
        return pprint(vars(self))