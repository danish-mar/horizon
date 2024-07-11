import hashlib


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
            transaction_id=db_result['transaction_id'],
            sender_account_id=db_result['sender_account_id'],
            receiver_account_id=db_result['receiver_account_id'],
            amount=db_result['amount'],
            transaction_type=db_result['transaction_type'],
            description=db_result.get('description', ''),
            created_at=db_result['created_at'],
            previous_hash=db_result['previous_hash']
        )

    def calculate_hash(self):
        hash_string = f"{self.transaction_id}{self.sender_account_id}{self.receiver_account_id}{self.amount}{self.transaction_type}{self.description}{self.created_at}{self.previous_hash}"
        return hashlib.sha256(hash_string.encode()).hexdigest()