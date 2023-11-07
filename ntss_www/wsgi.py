#!/usr/bin/env python3
"""
The NTSS app
Import all controllers that will have route defined for them
"""
from functools import wraps
from ntss.controllers.routes import Routes
from ntss.controllers.ntss import NtssController
from ntss.controllers.events import EventsController
# from ntss.controllers.users import UsersController


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
                return ntss_ctrl._redirect('/')
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
    print('aa: ', request)
    output = NtssController(request, response).login()
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


@application.route('/user/{user_id}', methods=['GET'])
def profile(request, response, user_id):
    """ The page to view a user's profile"""
    print(request.params)
    response.text = f'This is the profile management page for {user_id}'
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
