"""
The package to handle events
"""
from ntss.controllers.controller import BaseController
from ntss.views.events import EventViews

class EventsController(BaseController):
    """
    The controller for events
    """
    def __init__(self) -> None:
        """
        Initializes the events controller
        """
        super().__init__()
    
    def get_user_event(self, event_id):
        """
        Gets an event for a user
        """
        print(f'Call event model to get event info for {event_id}')
        event_info={
            'id': 12,
            'name': "Event XII",
            'description': '',
            'booths': 3,
            'start_date': 'Oct 23, 2023',
            'end_date': 'Oct 31, 2023',
            'location': 'Fayetteville, NC',
            'venue': 'Fayetteville State University'
        }
        return EventViews().user_event(event_info)

    def get_user_events(self):
        """
        Gets events that is associated with a user
        """
        return EventViews().user_events()

    def get_exhibitor_booth_invoice(self, event_id, invoice_id):
        """
        Gets an event for a user
        """
        event_info={
            'id': event_id,
            'name': "Event XII",
            'description': '',
            'booths': 3,
            'start_date': 'Oct 23, 2023',
            'end_date': 'Oct 31, 2023',
            'location': 'Fayetteville, NC',
            'venue': 'Fayetteville State University'
        }
        customer_info={
            'id': 345,
            'name': 'Jose\' Vargas',
            'address': '1234 Pelican Bay',
            'city': 'New York City',
            'state': 'New York',
            'zipcode': 1001
        }
        invoice_items = [{
            'name': 'Booth Reservation',
            'qty': event_info['booths'],
            'price': 45,
            'subtotal': (event_info['booths'] * 45)
        }]
        tax = 0
        subtotal = sum(item['subtotal'] for item in invoice_items)
        invoice_details = {
            'items': invoice_items,
            'total': round(subtotal * tax + subtotal, 2),
            'subtotal': subtotal,
            'tax': tax
        }
        invoice_information = {
            'id': invoice_id,
            'date': 'Oct 20, 2023',
            'event': event_info,
            'customer': customer_info,
            'invoice_details': invoice_details
        }
        return EventViews().display_invoice(invoice_information)
    # add other methods below
