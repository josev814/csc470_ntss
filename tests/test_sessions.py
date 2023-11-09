"""
Testing Session functionality
"""
import unittest
import time

from ntss_www.ntss.models.session import Session


class NTSSSessions(unittest.TestCase):
    """
    The class used for testing the session controller
    """
    def setUp(self):
        """
        Instead of calling __init__ we call setup
        Anything we define in here is what all the tests need to run
        """
        self._session_model = Session()
        self.session_id = ''
        self.session_data = {}

    def test_get_nonexistant_session(self):
        session_id = self._session_model._create_unique_id()
        session_info = self._session_model.get_session(session_id)
        self.assertFalse(session_info)

    def test_create_session(self):
        """
        Test creating session
        """
        self.session_data = {'logged_in': True}
        self.session_id = self._session_model.add_session(self.session_data)
        self.assertRegex(self.session_id, r'^[a-z0-9A-Z]+$')

    def test_remove_session(self):
        self.test_create_session()
        self._session_model.delete_session(self.session_id)
        self.assertFalse(self._session_model.get_session(self.session_id))

    def test_get_session(self):
        self.test_create_session()
        self.session_data = self._session_model.get_session(self.session_id)
        self.assertIn('logged_in', self.session_data)
        self.assertTrue(self.session_data['logged_in'])

    def test_update_session(self):
        self.test_create_session()
        self.session_data = self._session_model.get_session(self.session_id)
        self.session_data['logged_in'] = False
        self._session_model.update_session(self.session_id, self.session_data)
        new_data = self._session_model.get_session(self.session_id)
        self.assertFalse(new_data['logged_in'])
        self.assertEquals(self.session_data, new_data)

    def test_extend_session(self):
        self.test_create_session()
        current_expiration = self._session_model.get_session_expiration(self.session_id)
        time.sleep(1)
        self._session_model.renew_session(self.session_id)
        new_expiration = self._session_model.get_session_expiration(self.session_id)
        self.assertNotEqual(current_expiration, new_expiration)
        self.assertGreater(new_expiration, current_expiration)
        self._session_model.delete_session(self.session_id)
