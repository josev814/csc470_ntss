"""
This package handles interactions with the database pertaining to users
"""
from uuid import uuid4
import argon2
from ntss.models.database import MysqlDatabase


class Users(MysqlDatabase):
    """
    The Users class that interacts with the database
    """

    def __init__(self, debug=False):
        """
        When initializing the Users model set the default table to users
        """
        super().__init__(debug)
        self.set_table_metadata()
        self.set_table('users')

    def get_permissions(self, user_id):
        """
        Gets permissions for a user
        """
        self.set_table('user_permissions')
        query_filter = [
                {'column': 'user_id', 'operator': '=', 'value': user_id}
            ]
        permissions = self.db_select(
            ['*'],
            query_filter
        )
        return permissions

    def get_user(self, user_email: str, user_password: None) -> dict:
        """
        Retrieves a user from the database based on their user_email
        """
        user = {}
        records = self.get_user_by(email=user_email)
        for record in records:
            if user_password and self._check_password(user_password, record['password']):
                user = record
        return user

    def get_user_by_id(self, user_id: int) -> dict:
        """
        Retrieves a user from the database based on their user_id
        """
        user = []
        records = self.get_user_by(user_id=user_id)
        for record in records:
            user = record
        return user

    def get_user_by(self, user_id=None, email=None):
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
        records = self.db_select(
            filters=query_filter
        )
        return records
    
    def get_user_roles(self, user_id):
        """
        Gets the assigned roles for the current user
        """
        # TODO fix this
        print(f'Roles for {user_id}')
        return []
        

    def add_user(self, user_email: str, user_password: str) -> int:
        """
        Adds a user and returns their user_id from the database
        """
        self.db_create(
            {
                'user_email': user_email,
                'password': self._set_encrypted_password(user_password)
            }
        )
    
    def add_auth_token(self, auth_token: str, user_id: int) -> str:
        """
        Sets the auth token for a user
        """
        values = {'verification_code': auth_token}
        where_clause = [{'column': 'user_id', 'operator': '=', 'value': user_id}]
        records_updated = self.db_update(values, where_clause)
        print(f'ru: {records_updated}')


    @staticmethod
    def _set_encrypted_password(password: str):
        """
        Encrypts the password for a user
        """
        return argon2.PasswordHasher().hash(password)  # GOOD

    @staticmethod
    def _check_password(password: str, db_password: str) -> bool:
        """
        Checks if the password submitted is the same as the password that was stored
        """
        return_val = False
        try:
            argon2.PasswordHasher().verify(f'{db_password}', password)  # GOOD
            return_val = True
        except argon2.exceptions.VerifyMismatchError as msg:
            print(msg)
        return return_val

    @staticmethod
    def generate_auth_key() -> str:
        """
        Generates a hex unique identifier
        :return: str
        """
        return uuid4().hex
