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
    def __init__(self, key_filename, max_retries=5, retry_sleep=4):
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
            self._retry_count = 0
            return r.json()
        elif r.status_code == 403:
            raise Exception("Error 403: Forbidden!")
        elif self._retry_count < self.max_retires:  # retry if count < max
            sleeptime = self.retry_sleep
            self._retry_count += 1  # increment count
            print "Status code: %d, \t Retry count: %d" % (r.status_code, self._retry_count)
            print "Retrying in %0.2f seconds" % sleeptime
            time.sleep(sleeptime)  # Sleep to not inundate API
            return self._get_json(url)  # Retry called recursively
        elif r.status_code == 429:
            self._retry_count = 0
            raise Exception('Error 429: API rate limit reached!')
        else:
            self._retry_count = 0
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


    def get_summonerIds_by_match(self, matchId, team_with=None):
        """
        Get match data from API given a matchId and extract summonerIds from it. If team_with
        info is provided, this function returns summonerIds from the same team, including the team_with ID.
        Args:
            matchId: int of matchId
            team_with: summonerId of team member

        Returns:
            dict containing match data
        """
        summonerId_from_team = {100: [], 200: []}  # dict for team to summonerId mapping
        team_from_summonerId = {}  # dict for summonerId to team mapping

        match = self.get_match(matchId)

        if len(match['participants']) != len(match['participantIdentities']):
            Exception("Error: 'participants' and 'participantIdentities' len don't match ")

        for p_idx in range(len(match['participants'])):
            summonerId = match['participantIdentities'][p_idx]['player']['summonerId']
            teamId = match['participants'][p_idx]['teamId']
            summonerId_from_team[teamId] += [summonerId]
            team_from_summonerId[summonerId] = teamId

        if team_with == None:
            return summonerId_from_team[100] + summonerId_from_team[200]
        else:
            team_with_teamId = team_from_summonerId[team_with]
            return summonerId_from_team[team_with_teamId]

