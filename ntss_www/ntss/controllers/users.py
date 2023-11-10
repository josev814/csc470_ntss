"""
Package to handle Users
"""
from operator import is_
import re
from ntss.controllers.controller import BaseController
from ntss.views.users import UserViews
from ntss.models.user import Users as UserModel
from ntss.models.session import Session


class UsersController(BaseController):
    """
    This class handles anything pertaining to a user
    """
    _user_info = {}

    # add other methods below
    # Views should be placed in the views -> users.py file
    def get_user_roles(self, user_id: int):
        """
        Gets the role assigned to a user
        """
        roles = UserModel().get_user_roles(user_id)
        return roles

    def get_user_profile(self, user_id: int):
        """
        Gets the profile for a user
        """
        UserViews().get_user_profile(user_id)

    def validate_user(self, email: str, password: str):
        """
        Validate a user that is attempting to log in
        """
        self._user_info = UserModel().get_user(email, password)
        if not self._user_info:
            return False
        return True
    
    def valid_user(self, email: str = None) -> bool:
        """
        Checks if a user is valid
        """
        if email:
            self._user_info = UserModel().get_user_by(email=email)
        if len(self._user_info) > 0:
            return True
        return False

    def get_user_info(self, user_id):
        """
        Returns the current user's info
        """
        if not self._user_info:
            self._user_info = UserModel().get_user_by_id(user_id)
        return self._user_info

    def get_user_permissions(self, user_id: int):
        """
        Returns additional permissions for the user
        """

    def has_access(self, path: str) -> bool:
        """
        Returns if the current user has access
        """
        print(path)
        return True

    def create_session(self):
        """
        Creates a session for the user
        """
        user_session_data = self._user_info
        remove_items = ['password', 'create_date', 'updated_date']
        for remove_item in remove_items:
            if remove_item in user_session_data:
                del user_session_data[remove_item]
        session_id = Session().add_session(user_session_data)
        return session_id

    def add_auth_token(self):
        """
        Adds an auth token into the database
        """
        user_db = UserModel()
        auth_token = user_db.generate_auth_key()
        user_id = self._user_info[0]['user_id']
        user_db.add_auth_token(auth_token, user_id)
        return auth_token

    def add_user(self):
        """
        Adds a user into the system
        """
        posted_values = {}
        errors = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value
            is_valid, errors = self._verify_add_user_form(posted_values)
            if is_valid:
                user_guid = UserModel().add_user(posted_values['email'], posted_values['password'])
                if user_guid:
                    self.redirect(f'/users/edit/{user_guid}')

        return UserViews().add_user(posted_values, errors)

    def _verify_add_user_form(posted_values):
        """
        Verifies that we have all the data for the add user form
        """
        errors = []
        is_valid = True
        for key, val in posted_values:
            match key:
                case email:
                    if not re.match(r'[a-z0-9_\-\.]+@[a-z0-9_\-\.]+.[a-z0-9_\-]+', val, re.I):
                        errors.append('Email is invalid')
                    elif(len(UserModel().get_user_by(email=email)) > 0):
                        is_valid = False
            # TODO: Add more validations for this form
        if len(errors) > 0:
            is_valid = False
        return is_valid, errors

    def edit_user(self, user_guid):
        """
        Load a page to edit the user
        """
