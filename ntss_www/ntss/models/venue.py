"""
This package handles interactions with the database pertaining to users
"""
from ntss.models.database import MysqlDatabase


class Venue(MysqlDatabase):
    """
    The Venue class that interacts with the database
    """

    def __init__(self, debug=False):
        """
        When initializing the Users model set the default table to users
        """
        super().__init__(debug)
        self.set_table_metadata()
        self.set_table('venues')

    def get_venues(self, columns: list=[], start: int=0, limit: int=20) -> list:
        """
        Gets all venues from the database 
        """
        if columns:
            return self.db_select(columns, start=start, limit=limit)
        else:
            return self.db_select(start=start, limit=limit)

    def get_venue(self, venue_guid: str) -> dict:
        """
        Retrieves a venue from the database based on the venue guid
        """
        venue = {}
        records = self.get_venue_by(venue_guid=venue_guid)
        return records[0]

    def get_venue_by(self, name=None, city=None, state=None, guid=None, limit: int=1):
        """
        Performs a select query based on the params passed
        """
        query_filter = []
        if guid:
            query_filter.append(
                {'column': 'venue_guid', 'operator': '=', 'value': guid}
            )
        if name:
            query_filter.append(
                {'column': 'name', 'operator': '=', 'value': name}
            )
        if city:
            query_filter.append(
                {'column': 'city', 'operator': '=', 'value': city}
            )
        if state:
            query_filter.append(
                {'column': 'state', 'operator': '=', 'value': state}
            )
        records = self.db_select(
            filters=query_filter,
            limit=limit
        )
        return records
    
    def add(self, *args) -> str|bool:
        """
        Adds a venue and returns the venue_guid from the database
        """
        if len(args) == 1:
            args = args[0]
        else:
            raise IndexError('Too many indexes in the Tuple')

        guid = self.generate_guid()
        values = {
            'venue_guid': guid,
            'name': args.get('name'),
            'address': args.get('address'),
            'address2': args.get('address2'),
            'city': args.get('city'),
            'state': args.get('state'),
            'zip': args.get('zip'),
            'booths': args.get('booths'),
            'conference_rooms': args.get('conference_rooms'),
            'phone': args.get('phone'),
            'website': args.get('website'),
            'is_active': 1
        }
        if self.db_create(values):
            return guid
        return False
