"""
Simple API to access League of Legends data using Riot Games API

Author: Angad Gill
"""

import requests
import time

class RiotGames(object):
    """
    Simple class to access Riot Games API
    """
    def __init__(self, key_filename, max_retries=5, retry_sleep=2):
        """
        Initialize a RiotGames object. This is used to get data uding the API.

        :param key_filename: path to file containing API key stored on disk
        :param max_retries: max number of retries when getting data
        :param retry_sleep: seconds of sleep between retries
        """
        self.key = self._get_key(key_filename)
        self.max_retires = max_retries  # when getting data from server
        self._retry_count = 0  # current retry count
        self.retry_sleep = retry_sleep  # seconds between retries

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
        elif self._retry_count < self.max_retires:  # retry if count < max
            sleeptime = self.retry_sleep
            self._retry_count =+ 1  # increment count
            print "Retrying in %0.2f seconds" % sleeptime
            time.sleep(sleeptime)  # Sleep to not inundate API
            return self._get_json(url)  # Retry called recursively
        elif r.status_code == 429:
            raise Exception('API rate limit reached!')
        else:
            raise Exception('Connection error!')


    def get_static_match_data(self):
        """
        Get all static data provided by the API
        Returns:
            list of dicts containing match data.
        """
        matches = []

        def gen_static_url(num):
            url = 'https://s3-us-west-1.amazonaws.com/riot-api/seed_data/matches%d.json' % num
            return url

        for num in range(1, 11):
            url = gen_static_url(num)
            print "Fetching %s ..." % url
            r = requests.get(url)
            try:
                data = r.json()
                matches += data['matches']
                print "Done!"
            except:
                print "Error! Skipping."
            time.sleep(1)
        print "All done!"

        return matches


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

