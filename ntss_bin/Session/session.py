"""
"""
from uuid import uuid4
from webob import cookies


class Session:
    """
    """

    _session_cookie_name = 'ntss_session'
    _session_expiration = 7200 # expire after 2 hours
    _cookie = {}

    def __init__(self):
        cookies.make_cookie(
            name = self._session_cookie_name,
            value = '',
            max_age = self._session_expiration,
            path = '/',
            secure = True,
            httponly = True,
            comment = 'a comment',
            samesite = 'strict'
        )

    def regenerate(self, destroy: bool = False):
        """
        Regenerates the session ID.
        
        @param bool $destroy Should old session data be destroyed?
        """

    def destroy(self):
        """
        Destroy the current session
        """

    def set_session(self, data, value):
        """
        Sets user data into the session.

        If data is a string, then it is interpreted as a session property
        key, and  value is expected to be non-null.

        If data is an array, it is expected to be an array of key/value pairs
        to be set as session properties.
    
        @param array|string     data  Property name or associative array of properties
        @param any              value Property value if single key provided
        """

    def get_session(self, key: str):
        """
        Get user data that has been set in the session.
     
        If the property exists as "normal", returns it.
        Otherwise, returns an array of any temp or flash data values with the
        property key.
     
        @param string   key Identifier of the session property to retrieve
     
        @return any     The property value(s)
        """

    def has_key(self, key: str) -> bool:
        """
        Returns whether an index exists in the session dictionary.
        
        @param string   key Identifier of the session property we are interested in.

        @return bool    Returns if the session key exists
        """

    def remove_key(self, key: str|list) -> bool:
        """
        Remove one or more session properties.
        
        If key is a list, it is interpreted as a list of string property
        identifiers to remove. Otherwise, it is interpreted as the identifier
        of a specific session property to remove.
        
        @param list|string     key Identifier of the session property or properties to remove.
        """