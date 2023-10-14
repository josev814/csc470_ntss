#!/usr/bin/env python3
"""
The NTSS app
"""
import sys


sys.path.append('/var/www/html/public_html')

from ntss.controllers.routes import Routes
from ntss.controllers.ntss import NtssController


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
    print(request.params)
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

@application.route('/event/{id}/{name}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event(request, response, event_id, name):
    """ A page to list a particular event """
    print(request.params)
    response.text = f'This is the event management page for {event_id}: {name}'
