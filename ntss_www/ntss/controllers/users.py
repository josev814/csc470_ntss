"""
Package to handle Users
"""
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

    def get_user_profile(self, user_guid: str):
        """
        Gets the profile for a user
        """
        session_id = self._get_session_id()
        session_data = self._get_session_data(session_id)
        if user_guid != session_data["user_guid"]:
            # TODO: Pull data from database
            pass
        return UserViews().get_user_profile(session_data)
        
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
                posted_values[request_name] = request_value.strip()
            is_valid, errors = self._verify_add_user_form(posted_values)
            if is_valid:
                user_guid = UserModel().add_user(
                    posted_values['email'], posted_values['password'], posted_values
                )
                if user_guid:
                    print(f'redirecting to the edit user page for {user_guid}')
                    return self.redirect(f'/users/edit/{user_guid}')

        return UserViews().add_user(posted_values, errors)

    def _verify_add_user_form(self, posted_values):
        """
        Verifies that we have all the data for the add user form
        """
        errors = []
        is_valid = True
        for key, form_val in posted_values.items():
            match key:
                case 'email':
                    if not re.match(r'[a-z0-9_\-\.]+@[a-z0-9_\-\.]+.[a-z0-9_\-]+', form_val, re.I):
                        errors.append('Email is invalid')
                    elif(len(UserModel().get_user_by(email=form_val)) > 0):
                        errors.append('Email Already Exists')
                case other:
                    print(f"{other} isn't being validated on form submission")
            # TODO: Add more validations for this form
        if len(errors) > 0:
            is_valid = False
        print(errors)
        return is_valid, errors

    def edit_user(self, user_guid):
        """
        Load a page to edit the user
        """
        return f'Update the UserController::edit_user method to allow editing of user: {user_guid}'
        # TODO: this method needs to be flushed out

    def list_users(self, start: int=0):
        """
        Lists the users in the system
        """
        users_data = UserModel().get_users(start)
        # Get current user session
        # pass the user info to views
        # Ensure that the role for the user is detected in the navigation
        # TODO: use session to load current user info
        #sid = self._get_session_id()
        #session_data = self._get_session_data(sid)
        user_info = {'user_roles': 'NTSS_ADMIN'}
        print(users_data)
        return UserViews().list_users(users_data, user_info)
