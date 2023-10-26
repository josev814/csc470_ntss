"""
Package to handle Users
"""
from ntss.controllers.controller import BaseController
from ntss.views.users import UserViews
#from ntss.models.user import Users as UserModel

class UsersController(BaseController):
    """
    This class handles anything pertaining to a user
    """

    # add other methods below
    # Views should be placed in the views -> users.py file
    def get_user_roles(self, user_id: int):
        """
        Gets the role assigned to a user
        """

    def get_user_profile(self, user_id: int):
        """
        Gets the profile for a user
        """
        user_info = {
            'user_id': user_id,
            'name': 'My Name',
            'email': 'myemail@123.com'
        }
        return UserViews().get_user_profile(user_info)
