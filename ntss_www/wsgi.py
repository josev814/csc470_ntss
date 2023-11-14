#!/usr/bin/env python3
"""
The NTSS app
Import all controllers that will have route defined for them
"""
from functools import wraps
from ntss.controllers.routes import Routes
from ntss.controllers.ntss import NtssController
from ntss.controllers.events import EventsController
from ntss.controllers.users import UsersController
from ntss.controllers.venues import VenuesController


application = Routes()


def login_access_required(call_func):
    """
    Checks if the user is logged in for a route

    if the user is logged in and has access we call the route
    if the user is not logged in, we redirect to home
    """
    @wraps(call_func)
    def decorated_view(request, response, **kwargs):
        if request.path != '/':
            ntss_ctrl = NtssController(request, response)
            if not ntss_ctrl.is_logged_in() and not ntss_ctrl.get_permissions():
                # redirect to home to login
                return ntss_ctrl.redirect('/')
        return call_func(request, response, **kwargs)
    return decorated_view


def return_output(response, data, http_code=200):
    """
    Returns the output response if either the text or response object

    This is necessary when using headers for redirects
    """
    if isinstance(data, str):
        response.status_code = http_code
        response.text = data
    else:
        response = data
    return response


@application.route(path='/', methods=['GET', 'POST'])
def home(request, response):
    """ The homepage of the site """
    output = NtssController(request, response).login()
    # print(type(output))
    response = return_output(response, output, 200)
    return response


@application.route(path='/forgot_password', methods=['GET', 'POST'])
def forgot_password(request, response):
    """ The page for performing a request to reset the password """
    output = NtssController(request, response).forgot_password()
    # print(type(output))
    response = return_output(response, output, 200)
    return response


@application.route('/dashboard', methods=['GET'])
@login_access_required
def dashboard(request, response):
    """ The dashboard that is displayed when users first login"""
    print(request.path)
    output = NtssController(request, response).dashboard()
    response.text = output
    return response


@application.route('/users/add_user', methods=['GET','POST'])
@login_access_required
def add_user(request, response):
    """Route to direct to add user function"""
    output = UsersController(request, response).add_user()
    response = return_output(response, output, 200)
    return response

@application.route('/users/edit/{user_guid}', methods=['GET','POST'])
@login_access_required
def edit_user(request, response, user_guid: str):
    """
    Route to direct to edit user
    """
    # TODO: The methods for this need to be built out
    output = UsersController(request, response).edit_user(user_guid)
    response.text = output
    return response

@application.route('/users/delete/{user_guid}', methods=['GET','POST'])
@login_access_required
def delete_user(request, response, user_guid: str):
    """
    Route to delete a user
    """
    output = UsersController(request, response).delete_user(user_guid)
    response = return_output(response, output, 200)
    return response

@application.route('/users/view/{user_guid}', methods=['GET'])
def profile(request, response, user_guid):
    """ The page to view a user's profile"""
    print(request.params)
    output = UsersController(request, response).get_user_profile(user_guid)
    response.text = output
    return response


@application.route('/users/list_users', methods=['GET'])
def list_users(request, response):
    """ The page to view the list of users"""
    print(request.params)
    output = UsersController(request, response).list_users()
    response.text = output
    return response


@application.route('/events', methods=['GET'])
def events(request, response):
    """ The page to list events """
    print(request.params)
    response.text = 'This is the events management page'
    return response


@application.route('/event/{event_id}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event(request, response, event_id):
    """ A page to list a particular event """
    print(request.params)
    response.text = f'This is the event management page for {event_id}'


@application.route('/myevent/{event_id}/invoice/{invoice_id}', methods=['GET'])
def myinvoice(request, response, event_id, invoice_id):
    """ A page to print an invoice """
    print(request.path)
    output = EventsController(request, response).get_exhibitor_booth_invoice(event_id, invoice_id)
    response.text = output
    return response


@application.route('/myevent/{event_id}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def myevent(request, response, event_id):
    """ A page to list a particular event """
    print(request.path)
    output = EventsController(request, response).get_user_event(event_id)
    response.text = output
    return response


@application.route('/myevents', methods=['GET'])
def myevents(request, response):
    """ A page to display a user's events"""
    print(request.path)
    output = EventsController(request, response).get_user_events()
    response.text = output
    return response


@application.route('/logout', methods=['GET'])
def logout(request, response):
    """ Logs out a user """
    print(request.path)
    output = NtssController(request, response).logout()
    response = return_output(response, output, 200)
    return response


### VENUES ###
@application.route('/venues/list', methods=['GET'])
@login_access_required
def list_venues(request, response):
    """
    Lists the venues in the system
    """
    response.text = VenuesController(request, response).list()
    return response

@application.route('/venues/add', methods=['GET', 'POST'])
@login_access_required
def add_venue(request, response):
    """
    Adds a venue in the system
    """
    controller_response = VenuesController(request, response).add()
    response = return_output(response, controller_response, 200)
    return response

@application.route('/venue/view/{guid}', methods=['GET'])
@login_access_required
def get_venue(request, response, guid: str):
    """
    Gets the venue in the system based on the guid
    """
    response.text = VenuesController(request, response).view(guid)
    return response

@application.route('/venue/edit/{guid}', methods=['GET', 'POST'])
@login_access_required
def edit_venue(request, response, guid: str):
    """
    Processes an edit for a venue in the system based on the guid
    """
    response.text = VenuesController(request, response).edit(guid)
    return response

@application.route('/venue/delete/{guid}', methods=['GET', 'POST'])
@login_access_required
def delete_venue(request, response, guid: str):
    """
    Deletes a venue in the system based on the guid
    """
    controller_response = VenuesController(request, response).delete(guid)
    response = return_output(response, controller_response, 200)
    return response

### END VENUES ###
