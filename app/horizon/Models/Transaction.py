import hashlib
from pprint import pprint

class Transaction:
    def __init__(self, transaction_id, sender_account_id, receiver_account_id, amount, transaction_type, description, created_at, previous_hash):
        self.transaction_id = transaction_id
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id
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
            sender_account_id=db_result[1],
            receiver_account_id=db_result[2],
            amount=db_result[3],
            transaction_type=db_result[4],
            description=db_result[5],
            created_at=db_result[6],
            previous_hash=db_result[7]
        )

    def calculate_hash(self):
        hash_string = f"{self.transaction_id}{self.sender_account_id}{self.receiver_account_id}{self.amount}{self.transaction_type}{self.description}{self.created_at}{self.previous_hash}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def __str__(self):
        return pprint(vars(self))