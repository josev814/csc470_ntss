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
    output = NtssController().login(request)
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/dashboard', methods=['GET'])
def dashboard(request, response):
    #response.text = 'This is the dashboard'
    output = NtssController().dashboard()
    response.status_code = 200
    response.text = output
    return [output]

@application.route('/profile', methods=['GET'])
def profile(request, response):
    response.text = 'This is the profile management page'

@application.route('/events', methods=['GET'])
def events(request, response):
    response.text = 'This is the events management page'

@application.route('/event/{id}/{name}', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event(request, response, event_id, name):
    print(request.params)
    print(request.query_string)
    response.text = f'This is the event management page for {event_id}: {name}'
