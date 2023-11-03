"""
This package handles interactions with the database pertaining to users
"""
from argon2 import PasswordHasher
from uuid import uuid4
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
        user = []
        records = self._get_user_by(email=user_email)
        for record in records:
            if not user_password or \
                    (user_password and self._check_password(user_password, record['password'])):
                user = record
        return user
    
    def get_user_by_id(self, user_id: int) -> dict:
        """
        Retrieves a user from the database based on their user_id
        """
        user = []
        records = self._get_user_by(user_id=user_id)
        for record in records:
            user = record
        return user

    def _get_user_by(self, user_id=None, email=None):
        """
        Performs a select query based on the params passed
        """
        query_filter = []
        if user_id:
            query_filter.append(
                {'column': 'user_id', 'operator': '=', 'value': user_id}
            )
        if email:
            query_filter.append(
                {'column': 'email', 'operator': '=', 'value': email}
            )
        records = self.select(
            '*',
            query_filter
        )
        return records

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

    @staticmethod
    def _set_encrypted_password(self, password: str):
        """
        Encrypts the password for a user
        """
        return PasswordHasher().hash(password)  # GOOD

    @staticmethod
    def _check_password(self, password: str, encrypted_password) -> bool:
        """
        Checks if the password submitted is the same as the password that was stored
        """
        return PasswordHasher().verify(encrypted_password, password)  # GOOD

    @staticmethod
    def generate_auth_key(self) -> str:
        """
        Generates a hex unique identifier
        :return: str
        """
        return uuid4().hex
