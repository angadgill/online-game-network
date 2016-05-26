"""
Script to remove unwanted data from matches object. This script will keep the following data:
    matchId, summonerId, champLevel, and winner

Usage:
    `python reduce_matches 2`   where 2 is the saved state number. the script will load 'matches_2', extract the
    relevant data and save it in 'matches_reduced'. If 'matches_reduced' already exists, the script will append it.


Author: Angad Gill
"""
import sys
import utils


def main(state_num):
    matches_filename = 'matches_%d' % state_num
    print 'Loading %s ...' % matches_filename
    matches = utils.load_data(matches_filename)

    matches_reduced_filename = 'matches_reduced'
    try:
        print "Loading matches_reduced ..."
        matches_reduced = utils.load_data(matches_reduced_filename)
    except:
        print "Matches_reduced doesn't exists, creating new."
        matches_reduced = {}

    num_matches = len(matches.keys())

    for keyIdx, matchId in enumerate(matches.keys()):
        print "\rMatch %d out of %d [%0.1f%%]" % (keyIdx + 1, num_matches, (keyIdx + 1) / float(num_matches) * 100),

        summoners = []
        num_summoners = len(matches[matchId]['participants'])
        for i in range(num_summoners):
            champLevel = matches[matchId]['participants'][i]['stats']['champLevel']
            summonerId = matches[matchId]['participantIdentities'][i]['player']['summonerId']
            winner = matches[matchId]['participants'][i]['stats']['winner']
            summoners += [{'champLevel': champLevel, 'summonerId': summonerId, 'winner': winner}]
        matches_reduced[matchId] = {'summoners': summoners}

    print "Saving %s ..." % matches_reduced_filename
    utils.save_data(matches_reduced, matches_reduced_filename)
    print "Done!"


if __name__ == '__main__':
    state_num = int(sys.argv[1])
    main(state_num)