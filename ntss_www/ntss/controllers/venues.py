"""
Package to handle Users
"""
import re
from ntss.controllers.controller import BaseController
from ntss.views.venues import VenueViews
from ntss.models.venue import Venue as VenueModel
from ntss.models.session import Session


class VenuesController(BaseController):
    """
    This class handles anything pertaining to a venue
    """
    _venue_info = {}

    # add other methods below
    # Views should be placed in the views -> venues.py file
    def add(self):
        """
        Adds a venue into the system
        """
        posted_values = {}
        errors = None
        if self._request.method == 'POST':
            for request_name, request_value in self._request.params.items():
                posted_values[request_name] = request_value.strip()
            is_valid, errors = self._verify_add_form(posted_values)
            if is_valid:
                venue_guid = VenueModel().add(
                    posted_values
                )
                if venue_guid:
                    return self.redirect('/venues/list')

        return VenueViews(self._session_data).add(posted_values, errors)

    def _verify_add_form(self, posted_values):
        """
        Verifies that we have all the data for the add user form
        """
        errors = []
        is_valid = True
        if(len(VenueModel().get_venue_by(name=posted_values.get('name'), city=posted_values.get('city'), state=posted_values.get('state'))) > 0):
            errors.append('Venue already exists in this city')
            # TODO: Add more validations for this form
        if len(errors) > 0:
            is_valid = False
        return is_valid, errors

    def edit(self, guid):
        """
        Load a page to edit the venue
        """
        venue_data = {}
        errors = None
        try:
            venue_data = VenueModel().get_venue_by(guid=guid)
            if len(venue_data) == 0:
                raise Exception
            venue_data = venue_data[0]
        except:
            return VenueViews(self._session_data).not_found(guid)

        if self._request.method == 'POST':
            form_data = {}
            for request_name, request_value in self._request.params.items():
                form_data[request_name] = request_value.strip()
            is_valid, errors = self._verify_edit_form(form_data)
            if is_valid:
                if VenueModel().update(guid, form_data):
                    venue_data = form_data
                    venue_data['venue_guid'] = guid
                    errors.append('Record Successfully Updated')
        return VenueViews(self._session_data).edit(venue_data, errors)
    
    def _verify_edit_form(self, posted_values):
        """
        Verifies that we have all the data for the add user form
        """
        errors = []
        is_valid = True
        if len(posted_values) < 12:
            errors.append('Invalid form post')
        if len(errors) > 0:
            is_valid = False
        return is_valid, errors

    def list(self, start: int=0):
        """
        Lists the venues in the system
        """
        columns = ['venue_guid', 'name', 'city', 'state', 'create_date', 'is_active']
        venue_data = VenueModel().get_venues(columns=columns, start=start)
        return VenueViews(self._session_data).list(venue_data)

    def view(self, guid):
        """
        Load a page to view the venue
        """
        try:
            venue_data = VenueModel().get_venue(guid)
            return VenueViews(self._session_data).get_venue(venue_data)
        except:
            return VenueViews(self._session_data).not_found(guid)
    
    def delete(self, guid):
        """
        Delete a venue
        """
        try:
            venue_data = VenueModel().get_venue_by(guid=guid)
            if len(venue_data) == 0:
                raise Exception
            if not VenueModel().delete(guid):
                raise Exception
            return self.redirect('/venues/list')
        except:
            return VenueViews(self._session_data).not_found(guid)
