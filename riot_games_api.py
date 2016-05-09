"""
Simple API to access League of Legends data using Riot Games API

Author: Angad Gill
"""


import requests


class RiotGames(object):
    """
    Simple class to access Riot Games API
    """
    def __init__(self, key_filename):
        self.key = self._get_key(key_filename)


    def _get_key(self, key_filename):
        """
        Imports API key stored in a file on disk
        :param key_filename: name of the file which stores the key
        :return: string. API key value.
        """
        with open(key_filename, 'r') as f:
            return f.read()


    def _get_json(self, url):
        """
        Get data from the provided url and convert it to JSON if possible.
        :param url: RiotGame API endpoint (should include the API key)
        :return: Dict containing the data requested
        """
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            raise Exception('API rate limit reached!')
        else:
            raise Exception('Connection error!')


    def get_matches_by_summoner(self, summonerId):
        """
        Get match data from API given a summonerId.
        :param summonerId: int of summonerId
        :return: list of dicts containing match data
        """
        url = 'https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/%d?api_key=%s' % \
              (summonerId, self.key)
        matches = self._get_json(url)['matches']
        return matches


    def get_matchIds_by_summoner(self, summonerId):
        """
        Get match data from API given a summonerId and extract matchIds.
        :param summonerId: int of summonerId
        :return: list of ints containing matchIds
        """
        matches = self.get_matches_by_summoner(summonerId)
        matchIds = [m['matchId'] for m in matches]
        return matchIds


    def get_match(self, matchId):
        """
        Get full match data from API given a matchId.
        :param matchId: int of matchId
        :return: dict containing match data
        """
        url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/%d?api_key=%s' % \
              (matchId, self.key)
        match = self._get_json(url)
        return match


    def get_summonerIds_by_match(self, matchId):
        """
        Get match data from API given a matchId and extract summonerIds from it.
        :param matchId: int of matchId
        :return: list of ints containing summonerIds
        """
        summonerIds = []
        match = self.get_match(matchId)
        for p in match['participantIdentities']:
            summonerIds += [p['player']['summonerId']]
        return summonerIds

