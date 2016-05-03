"""
Class definitions and helper functions to access Battle.net API

Reference: https://dev.battle.net/io-docs

Author: Angad Gill
Inspired by: https://github.com/vishnevskiy/battlenet
"""


import requests


class BattleNet(object):
    """
    Main class that defines fetch methods and connection
    parameters.
    """
    def __init__(self, public_key):
        self.public_key = public_key
        self.locale = 'en_US'
        self.base_url = 'https://us.api.battle.net/wow/'

    def _url(self, concept):
        url = self.base_url + concept + '?locale=' + self.locale + '&apikey=' + self.public_key
        return url

    def realms(self):
        """
        Fetch information about all realms.
        :return: dict contain realm information.
        """
        url = self._url('realm/status')
        r = requests.get(url)
        realms = r.json()['realms']  # List of dicts
        return realms
