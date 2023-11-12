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
        self.template_vars['user'] = user_info
        return self.template.render(self.template_vars)
    
    def add_user(self, posted_values, errors: list):
        """
        Add a user into system
        """
        self.set_template('add_user.html')
        self.template_vars['pageName'] = 'Add User'
        self.template_vars['states'] = self.US_STATES
        self.template_vars['roles'] = self.ROLES
        self.template_vars['form_post'] = posted_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)
    
    def list_users(self, users: list, current_user: dict):
        """
        List users in the system
        """
        self.set_template('list_users.html')
        self.template_vars['pageName'] = 'List Users'
        self.template_vars['users'] = users
        self.template_vars['current_user'] = current_user
        return self.template.render(self.template_vars)
