"""
Package for User Views
"""
from ntss.views.views import Views


class UserViews(Views):
    """
    The class for handling views for users
    """

    def __init__(self, session_info: dict|None=None):
        super().__init__()
        self._user_session = session_info
        self._controller_type = 'users'
        self.template_vars['states'] = self.US_STATES
        self.template_vars['current_user'] = self._user_session

    def get_user_profile(self, user_session, user_info):
        """
        Load the the profile for a user
        """
        self.set_template('users/user_profile.html')
        self.template_vars['states'] = self.US_STATES
        self.template_vars['roles'] = self.ROLES
        self.template_vars['user'] = user_info
        self.template_vars['current_user'] = user_session
        self.template_vars['disable_form'] = True
        return self.template.render(self.template_vars)

    def add_user(self, user_session, posted_values, errors: list):
        """
        Add a user into system
        """
        self.set_template('users/add_user.html')
        self.template_vars['pageName'] = 'Add User'
        self.template_vars['states'] = self.US_STATES
        self.template_vars['roles'] = self.ROLES
        self.template_vars['current_user'] = user_session
        self.template_vars['form_post'] = posted_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def edit_user(self, user_session, user_values, errors: list):
        """
        Edit a user in the system
        """
        self.set_template('users/edit_user.html')
        self.template_vars['pageName'] = 'Edit User'
        self.template_vars['states'] = self.US_STATES
        self.template_vars['roles'] = self.ROLES
        self.template_vars['current_user'] = user_session
        self.template_vars['form_post'] = user_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def list_users(self, users: list, current_user: dict):
        """
        List users in the system
        """
        self.set_template('users/list_users.html')
        self.template_vars['pageName'] = 'List Users'
        self.template_vars['users'] = users
        self.template_vars['current_user'] = current_user
        return self.template.render(self.template_vars)

    def register_user(self, posted_values, errors):
        """
        Register user into system
        """
        self.set_template('ntss/register.html')
        self.template_vars['pageName'] = 'Register'
        self.template_vars['states'] = self.US_STATES
        new_roles = []
        for role in self.ROLES:
            if role not in ['NTSS_ADMIN', 'EVENT_STAFF']:
                new_roles.append(role) 
        self.template_vars['roles'] = new_roles
        self.template_vars['form_post'] = posted_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)   

    def list_exhibits(self, events):
        """
        Lists exhibits for a user
        """
        if self._user_session['user_roles'] not in ['NTSS_ADMIN', 'EVENT_STAFF', 'EXHIBITOR']:
            self.set_template('access_denied.html')
            return self.template.render(self.template_vars)

        self.set_template('events/exhibits/exhibitors_list.html')
        self.template_vars['pageName'] = 'Exhibits'
        self.template_vars['events'] = events
        return self.template.render(self.template_vars)

    def view_exhibit(self, exhibit):
        """
        View a particular exhibit
        """
        if self._user_session['user_roles'] not in ['NTSS_ADMIN', 'EVENT_STAFF', 'EXHIBITOR']:
            self.set_template('access_denied.html')
            return self.template.render(self.template_vars)

        self.set_template('events/exhibits/view_exhibit.html')
        self.template_vars['pageName'] = f'Exhibit {exhibit["transaction_guid"]}'
        self.template_vars['exhibit'] = exhibit
        return self.template.render(self.template_vars)

class UserSpeeches(Views):
    """
    class for Speeches in Views
    """

    def __init__(self, session_info: dict):
        super().__init__()
        self._user_session = session_info
        self._controller_type = 'speeches'
        self.template_vars['current_user'] = self._user_session

    def list_speeches(self, speeches: list) -> str:
        """
        List events in the system
        """
        self.template_vars['pageName'] = 'List Speech Proposals'
        self.template_vars['speeches'] = speeches
        if len(speeches) > 0:
            self.set_template('speeches/speech_list.html')
            return self.template.render(self.template_vars)
        self.set_template('speeches/no_speech_found.html')
        self.template_vars['controller_type'] = self._controller_type
        return self.template.render(self.template_vars)

    def add_speech(self, form_values, events, errors: list):
        """
        adds speech into system based on user
        """
        self.set_template('speeches/add_edit_speech.html')
        self.template_vars['pageName'] = 'Add Speech Proposal'
        self.template_vars['events'] = events
        self.template_vars['form_post'] = form_values
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def edit_speech(self, speech_values, events, errors: list):
        """
        edit speech in system based on user
        """
        self.set_template('speeches/add_edit_speech.html')
        self.template_vars['pageName'] = 'Edit Speech Proposal'
        self.template_vars['form_post'] = speech_values
        self.template_vars['events'] = events
        self.template_vars['errors'] = errors
        return self.template.render(self.template_vars)

    def view_speech_info(self, speech_info):
        """
        view speech info
        """
        self.set_template('speeches/speech_view.html')
        self.template_vars['pageName'] = f'Speech: {speech_info["speech_name"]}'
        self.template_vars['speech_info'] = speech_info
        return self.template.render(self.template_vars)


    def no_speech_found(self, speech_guid):
        """
        Shows the not found page if the speech doesn't exist
        """
        self.set_template('speeches/no_speech_found.html')
        self.template_vars['pageName'] = 'Speech Not Found'
        self.template_vars['guid'] = speech_guid
        return self.template.render(self.template_vars)
