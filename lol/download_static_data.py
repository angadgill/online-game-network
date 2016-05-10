"""
Download static data for League of Legends and store it as a pickled object.

Author: Angad Gill
"""

import riot_games_api
import utils

if __name__ == '__main__':
    rg = riot_games_api.RiotGames('riot_games_api.key')
    matches =  rg.get_static_match_data()
    utils.save_data(matches, 'static_matches.data')
