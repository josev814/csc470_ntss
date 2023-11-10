"""
Package for User Views
"""
from ntss.views.views import Views


class UserViews(Views):
    """
    The class for handling views for users
    """

    def get_user_profile(self, user_info):
        """
        Load the the profile for a user
        """
        self.set_template('user_profile.html')
        self.template_vars['states'] = self.US_STATES
        self.template_vars['roles'] = self.ROLES
        self.template_vars['user'] = user_info
        print(user_info)
        return self.template.render(self.template_vars)
