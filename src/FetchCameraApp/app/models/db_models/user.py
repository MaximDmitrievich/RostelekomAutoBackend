class User:
    def __init__(self, username, address):
        self._username = username
        self._address = address

    @property
    def username(self):
        return self._username
    
    @property
    def address(self):
        return self._address
