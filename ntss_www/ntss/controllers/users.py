"""
Package to handle Users
"""
from ntss.controllers.controller import BaseController
from ntss.views.users import UserViews
from ntss.models.user import Users as UserModel


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
        # self._user_info = UserModel().get_user(email, password)
        return True
    
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
