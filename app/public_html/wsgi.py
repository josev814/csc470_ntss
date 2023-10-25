#!/usr/bin/env python3
"""
The NTSS app
"""
import sys

from ntss.controllers.routes import Routes
from ntss.controllers.ntss import NtssController
from ntss.controllers.events import EventsController
from ntss.controllers.users import UsersController


application=Routes()

@application.route(path='/', methods=['GET', 'POST'])
def home(request, response):
    """ The homepage of the site """
    output = NtssController().login(request)
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/dashboard', methods=['GET'])
def dashboard(request, response):
    """ The dashboard that is displayed when users first login"""
    print(request.path)
    output = NtssController().dashboard()
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/user/{id}', methods=['GET'])
def profile(request, response):
    """ The page to view a user's profile"""
    print(request.params)
    response.text = 'This is the profile management page'

@application.route('/events', methods=['GET'])
def events(request, response):
    """ The page to list events """
    print(request.params)
    response.text = 'This is the events management page'

@application.route('/event/{event_id}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event(request, response, event_id):
    """ A page to list a particular event """
    print(request.params)
    response.text = f'This is the event management page for {event_id}'

@application.route('/myevent/{event_id}/invoice/{invoice_id}', methods=['GET'])
def myinvoice(request, response, event_id, invoice_id):
    """ A page to print an invoice """
    print(request.path)
    output = EventsController().get_exhibitor_booth_invoice(event_id, invoice_id)
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/myevent/{event_id}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def myevent(request, response, event_id):
    """ A page to list a particular event """
    print(request.path)
    output = EventsController().get_user_event(event_id)
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/myevents', methods=['GET'])
def myevents(request, response):
    """ A page to display a user's events"""
    print(request.path)
    output = EventsController().get_user_events()
    response.status_code = 200
    response.text = output
    return [output]
