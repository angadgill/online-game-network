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

    def _get_data(self, url, dict_key):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Connection error!')
        else:
            return r.json()[dict_key]

    def realms(self):
        """
        Fetch information about all realms.
        :return: dict contain realm data.
        """
        url = self._url('realm/status')
        realms = self._get_data(url, 'realms')  # List of dicts
        return realms

    def challenges(self, realm):
        """
        Fetch information about all challenges in a realm.
        :param realm:
        :return: dict containing challenge data
        """
        url = self._url('challenge/' + realm)
        challenges = self._get_data(url, 'challenge')  # List of dicts
        return challenges
