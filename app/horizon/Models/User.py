class User:


    '''
    User Class
    '''

    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.connected_account = None
        self.email = None
        self.address = None
        self.phone = None


    def get_user_id(self):
        return self.user_id

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_connected_account(self):
        return self.connected_account

    def get_email(self):
        return self.email

    def get_address(self):
        return self.address

    def get_phone(self):
        return self.phone
