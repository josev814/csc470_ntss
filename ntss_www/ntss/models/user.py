"""
This package handles interactions with the database pertaining to users
"""
from argon2 import PasswordHasher
from ntss.models.database import MysqlDatabase


class Users(MysqlDatabase):
    """
    The Users class that interacts with the database
    """

    def __init__(self):
        """
        When initializing the Users model set the default table to users
        """
        super().__init__()
        self.table = 'users'

    def get_permissions(self, user_id):
        """
        Gets permissions for a user
        """
        self.table = 'user_permissions'
        query_filter = [
                {'column': 'user_id', 'operator': '=', 'value': user_id}
            ]
        permissions = self.select(
            '*',
            query_filter
        )
        return permissions

    def get_user(self, user_email: str, user_password: None) -> dict:
        """
        Retrieves a user from the database based on their user_email
        """
        query_filter = [
                {'column': 'email', 'operator': '=', 'value': user_email}
            ]
        records = self.select(
            '*',
            query_filter
        )
        user = []
        for record in records:
            if not user_password or \
                    (user_password and self._check_password(user_password, record['password'])):
                user = record
        return user

    def add_user(self, user_email: str, user_password: str) -> int:
        """
        Adds a user and returns their user_id from the database
        """
        self.create(
            {
                'user_email': user_email,
                'password': self._set_encrypted_password(user_password)
            }
        )

    def _set_encrypted_password(self, password: str):
        """
        Encrypts the password for a user
        """
        return PasswordHasher().hash(password)  # GOOD

    def _check_password(self, password: str, encrypted_password) -> bool:
        """
        Checks if the password submitted is the same as the password that was stored
        """
        return PasswordHasher().verify(encrypted_password, password)  # GOOD
