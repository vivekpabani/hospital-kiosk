import os
from social.backends.oauth import BaseOAuth2
from drchrono.settings import SOCIAL_AUTH_DRCHRONO_KEY, SOCIAL_AUTH_DRCHRONO_SECRET

class drchronoOAuth2(BaseOAuth2):
    """
    drchrono OAuth authentication backend
    """

    name = 'drchrono'
    AUTHORIZATION_URL = 'https://drchrono.com/o/authorize/'
    ACCESS_TOKEN_URL = 'https://drchrono.com/o/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    USER_DATA_URL = 'https://drchrono.com/api/users/current'
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires_in')
    ]

    CLIENT_ID = SOCIAL_AUTH_DRCHRONO_KEY
    CLIENT_SECRET = SOCIAL_AUTH_DRCHRONO_SECRET

    def get_user_details(self, response):
        """
        Return user details from drchrono account
        """
        return {'username': response.get('username'),}

    def user_data(self, access_token, *args, **kwargs):
        """
        Load user data from the service
        """
        return self.get_json(
            self.USER_DATA_URL,
            headers=self.get_auth_header(access_token)
        )

    def get_auth_header(self, access_token):
        return {'Authorization': 'Bearer {0}'.format(access_token)}
