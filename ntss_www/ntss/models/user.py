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

    def get_users(self, columns: list=None, start=0, limit=20):
        """
        Gets all users free m the database 
        """
        user_records = self.db_select(columns=columns, start=start, limit=limit)
        return user_records

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

    def get_user_by(self, user_id=None, email=None, user_guid=None, limit=1):
        """
        Performs a select query based on the params passed
        """
        query_filter = []
        if user_id:
            query_filter.append(
                {'column': 'user_id', 'operator': '=', 'value': user_id}
            )
        if user_guid:
            query_filter.append(
                {'column': 'user_guid', 'operator': '=', 'value': user_guid}
            )
        if email:
            query_filter.append(
                {'column': 'email', 'operator': '=', 'value': email}
            )
        records = self.db_select(
            filters=query_filter,
            limit=limit
        )
        return records

    def get_user_roles(self, user_id):
        """
        Gets the assigned roles for the current user
        """
        # TODO fix this
        print(f'Roles for {user_id}')
        return []

    def add_user(self, user_email: str, user_password: str, *args) -> str|bool:
        """
        Adds a user and returns their user_id from the database
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')

        user_guid = self.generate_auth_key()
        user_values = {
            'email': user_email,
            'password': self._set_encrypted_password(user_password),
            'user_guid': user_guid,
            'prefix_name': args.get('prefix'),
            'first_name': args.get('firstName'),
            'middle_name': args.get('middleInitial'),
            'last_name': args.get('lastName'),
            'suffix_name': args.get('suffix'),
            'address': args.get('address'),
            'address2': args.get('secondAddress'),
            'city': args.get('city'),
            'state': args.get('state'),
            'zip': args.get('zipCode'),
            'phone': args.get('phoneNumber'),
            'website': args.get('website'),
            'user_roles': args.get('user_role'),
            'is_active': 1
        }
        if self.db_create(user_values):
            return user_guid
        return False

    def edit_user(self, *args) -> bool:
        """
        Edits user in database
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')

        user_values = {
            'email': args.get('email'),
            'prefix_name': args.get('prefix_name'),
            'first_name': args.get('first_name'),
            'middle_name': args.get('middle_name'),
            'last_name': args.get('last_name'),
            'suffix_name': args.get('suffix_name'),
            'address': args.get('address'),
            'address2': args.get('address2'),
            'city': args.get('city'),
            'state': args.get('state'),
            'zip': args.get('zip'),
            'phone': args.get('phone'),
            'website': args.get('website'),
            'user_roles': args.get('user_roles'),
            'is_active': args.get('is_active')
        }
        if args.get('password') is not None:
            user_values['password'] = self._set_encrypted_password(args.get('password'))

        where_clause = [{'column': 'user_guid', 'operator': '=', 'value': args.get('user_guid')}]

        return bool(self.db_update(user_values, where_clause))

    def delete_user(self, user_guid):
        """
        Deletes the user from system
        """
        where_clause = [{'column': 'user_guid', 'operator': '=', 'value': user_guid}]
        return bool(self.db_delete(where_clause))

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

    def change_password(self, email, password):
        values = {'password': password}
        where_clause = [{'column': 'email', 'operator': '=', 'value': email}]
        return self.db_update(values, where_clause)
