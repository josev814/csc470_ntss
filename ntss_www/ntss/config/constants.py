"""
Define constants in this file that can be used across all of the classes

DO NOT put sensitive information in here like usernames, passwords, hashes or secrets
"""

WWW_PATH = '/app/ntss_www/'


SITE_INFO = {
    'protocol': 'http://',
    'hostname': 'localhost',
    'port': '8080'
}


ALL_HTTP_METHODS = (
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH'
)


ROLES = (
    'NTSS_ADMIN',
    'EVENT_STAFF',
    'EXHIBITOR',
    'DOMAIN_EXPERT',
    'SELECTED_SPEAKER',
    'OBSERVER'
)

COOKIE_INFO = {
    'name': 'ntss_session',
    'max_age': 3600,  # 1 hour
}


US_STATES = (
    'Alabama', 'Alaska', 'Arizona', 'Arkansas',
    'California', 'Colorado', 'Connecticut',
    'Washington DC', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
    'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
    'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming'
)
