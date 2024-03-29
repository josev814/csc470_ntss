"""
Package to handle Users
"""
import re
from ntss.controllers.controller import BaseController
from ntss.views.users import UserViews, UserSpeeches as SpeechesViews
from ntss.models.user import Users as UserModel, UserSpeeches as Speeches
from ntss.models.session import Session
from ntss.models.event import Event as EventModel
from ntss.controllers.events import ExhibitsController


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
        user_data = UserModel().get_user_by(user_guid=user_guid)
        if len(user_data) == 1:
            user_data = user_data[0]
        return UserViews().get_user_profile(self._session_data, user_data)

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
        print(f'Accessing path {path}')
        if 'user_roles' not in self._user_info or self._user_info['user_roles'] == 'OBSERVER':
            return False
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

    def register_user(self):
        """
        Register a user into the system
        """
        posted_values = {}
        message = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            is_valid, message = self._verify_add_user_form(posted_values)
            if is_valid:
                user_guid = UserModel(True).add_user(
                    posted_values['email'], posted_values['password'], posted_values
                )
                if user_guid:
                    message = "User registered successfully."
        return UserViews().register_user(posted_values, message)

    def _verify_register_user_form(self, posted_values):
        """
        Verifies that we have all the data for the register user form
        """
        errors = []
        is_valid = True
        for key, form_val in posted_values.items():
            match key:
                case 'email':
                    if not re.match(r'[a-z0-9_\-\.]+@[a-z0-9_\-\.]+.[a-z0-9_\-]+', form_val, re.I):
                        errors.append('Email is invalid')
                    elif len(UserModel().get_user_by(email=form_val)) > 0:
                        errors.append('Email Already Exists')
                case other:
                    print(f"{other} isn't being validated on form submission")
            # TODO: Add more validations for this form
        if len(errors) > 0:
            is_valid = False
        print(errors)
        return is_valid, errors

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
                    return self.redirect('/users/list_users')

        return UserViews().add_user(self._session_data, posted_values, errors)

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
                    elif len(UserModel().get_user_by(email=form_val)) > 0:
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
        errors = None
        user_info = UserModel().get_user_by(user_guid=user_guid)
        print(user_info)
        if len(user_info) > 0:
            user_info = user_info[0]
        else:
            errors = ['Invalid User']

        if self._request.method == 'POST':
            user_info = {}
            for request_name, request_value in self._request.params.items():
                user_info[request_name] = request_value.strip()
            print(user_info)
            is_valid, errors = self._verify_edit_user_form(user_info)
            if is_valid:
                if UserModel().edit_user(user_info):
                    errors = ['User Saved to System']
                else:
                    errors = ['Failed to save user info, try again']
        return UserViews().edit_user(self._session_data, user_info, errors)

    def _verify_edit_user_form(self, posted_values):
        """
        Verifies that we have all the data for the edit user form
        """
        errors = []
        is_valid = True
        for key, form_val in posted_values.items():
            match key:
                case 'email':
                    if not re.match(r'[a-z0-9_\-\.]+@[a-z0-9_\-\.]+.[a-z0-9_\-]+', form_val, re.I):
                        errors.append('Email is invalid')
                case other:
                    print(f"{other} isn't being validated on form submission")
            # TODO: Add more validations for this form
        if len(errors) > 0:
            is_valid = False

        return is_valid, errors

    def delete_user(self, user_guid):
        """
        Delete User from system
        """
        # TODO: check if user exists
        # If the user doesn't exist, go back to the edit page
        # otherwise, load the user model
        # then statement is called to delete from user model with the user_guid
        # on success, redirect to user's page

        if UserModel().delete_user(user_guid):
            return self.redirect('/users/list_users')
        return self.redirect(f'/users/edit_user{user_guid}')

    def list_users(self, start: int = 0):
        """
        Lists the users in the system
        """
        users_data = UserModel().get_users(start)
        return UserViews(self._session_data).list_users(users_data)

    def change_password(self, email, password) -> bool:
        """
        Function to change password
        """
        user_db = UserModel(True)
        return user_db.change_password(email, password)

    def get_my_exhibits(self):
        """
        Lists the exhibits for a user
        """
        events, transactions = ExhibitsController(self._request, self._response).get_user_exhibits(
            self._session_data['user_guid']
        )
        for i in range(len(events)):
            for transaction in transactions:
                if transaction['event_guid'] == events[i]['event_guid']:
                    events[i]['transactions'] = transaction
        return UserViews(self._session_data).list_exhibits(events)

    def get_exhibit(self, exhibit_guid):
        """
        Gets the exhibit for a user
        """
        event, transactions, owner = ExhibitsController(
            self._request, self._response
            ).get_exhibit(
                exhibit_guid
            )
        exhibit = transactions[0]
        exhibit['event'] = event
        exhibit['event_owner'] = owner[0]
        return UserViews(self._session_data).view_exhibit(exhibit)

    ### SPEECH ROUTES ###

    def list_speeches(self, start: int = 0):
        """
        Lists the speeches in the system
        """
        columns = ['speech_guid','speech_name', 'user_guid']
        db_speech_data = Speeches().get_speeches(columns=columns, start=start)
        speech_data = db_speech_data
        if self._session_data['user_roles'] == 'SELECTED_SPEAKER':
            speech_data = []
            for speech in db_speech_data:
                print(speech)
                if speech['user_guid'] == self._session_data['user_guid']:
                    speech_data.append(speech)
        return SpeechesViews(self._session_data).list_speeches(speech_data)

    def add_speech(self):
        """
        Add speech into system 
        """
        posted_values = {}
        errors = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            speech_guid = Speeches().add_speech(posted_values)
            if speech_guid:
                print(f'redirecting to the edit user page for {speech_guid}')
                return self.redirect('/speeches/list')
        columns = ['event_guid', 'name']
        events = EventModel().get_events(columns=columns)
        return SpeechesViews(self._session_data).add_speech(posted_values, events, errors)

    def edit_speech(self, speech_guid):
        """
        edit speech in system
        """
        posted_values = {}
        errors = []
        speech_info = Speeches().get_speech_by(speech_guid=speech_guid)

        if len(speech_info) == 0:
            return SpeechesViews(self._session_data).no_speech_found(speech_guid)
        speech_info = speech_info[0]

        columns = ['event_guid', 'name']
        events = EventModel().get_events(columns=columns)

        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            speech_info = posted_values

            if Speeches().edit_speech(speech_guid, posted_values):
                errors.append('Event was successfully Updated')
        print(speech_info)

        return SpeechesViews(self._session_data).edit_speech(speech_info, events, errors)


    def view_speech_info(self, speech_guid):
        """
        view speech info
        """
        speech_info = Speeches().get_speech_by(speech_guid)
        if len(speech_info) == 0:
            return SpeechesViews(self._session_data).no_speech_found(speech_guid)
        speech_info = speech_info[0]
        event = EventModel().get_event_by(guid=speech_info['event_guid'])[0]
        speech_info['event'] = event
        return SpeechesViews(self._session_data).view_speech_info(speech_info)
    
    def delete_speech(self, speech_guid):
        """
        delete speech by guid
        """
        if Speeches().delete_speech(speech_guid):
            return self.redirect('/speeches/list')
        return self.redirect(f'/speeches/edit/{speech_guid}')
