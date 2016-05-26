"""
Miscellaneous utility functions are written here.

Author: Angad Gill
"""

import pickle


def save_data(data, filename):
    """
    Dumps data into filename using pickle
    Args:
        data:
        filename:

    Returns:
        nothing
    """
    with open(filename, 'w') as f:
        pickle.dump(data, f)


def load_data(filename):
    """
    Loads data from filename stored using pickle
    Args:
        filename:

    Returns:
        data
    """
    with open(filename, 'r') as f:
        data = pickle.load(f)
    return data


def list_of_dict_to_dict(list_of_dict, key):
    """
    Converts a list of dicts to a dict of dicts based on the key provided.
    Also removes the key from the nested dicts.
    converts [{key: v1, k2:v12, k3:v13}, {key:v2, k2: v22, k3:v23}, ... ]
      to {v1: {k2: v12, k3:v13}, v2:{k2:v22, k3:v23}, ...}
    Args:
        list_of_dict: eg: [{k1: v1, k2:v12, k3:v13}, {k1:v2, k2: v22, k3:v23}, ... ]

    Returns:
        dict_of_dict: eg: {v1: {k2: v12, k3:v13}, v2:{k2:v22, k3:v23}, ...}
    """
    dict_of_dict = {}

    for item in list_of_dict:  # item will be the nested dict
        value = item[key]  # This will be the "key" in dict_of_dict
        item.pop(key)  # removes key from the nested dict
        dict_of_dict[value] = item  # adds item to the new dict

    return dict_of_dict


def dict_values_to_lists(input_dict):
    """
    Converts all values in the dict to a list containing the value.

    Args:
        input_dict: any dict

    Returns:
        dict with values converted to lists
    """
    if input_dict is None:
        return None

    for key in input_dict.keys():
        input_dict[key] = [input_dict[key]]

    return input_dict


def dict_append_to_value_lists(dict_appendee, dict_new):
    """
    Appends values from dict_new to list of values with same key in dict_appendee
    Args:
        dict_appendee: dict with value lists (as created by dict_values_to_lists function
        dict_new: dict with new values that need to be appended to dict_appendee

    Returns:
        dict with appended values
    """
    if dict_new is None:
        return None

    for key in dict_new.keys():
        if type(dict_appendee[key]) != list:
            raise TypeError("Dict value is not a list")

        dict_appendee[key] += [dict_new[key]]

    return dict_appendee


def load_state(checkpoint_num):
    """
    Load data structures from disk using a checkpoint number.
    Args:
        checkpoint_num:

    Returns:
        matches, discovered_summonerIds, g, max_hop, bfs_queue, hop
    """
    print "Loading data from checkpoint %d ..." % checkpoint_num
    # matches = utils.load_data('matches_' + str(checkpoint_num))
    matches = {}
    discovered_summonerIds = utils.load_data('discovered_summonerIds_' + str(checkpoint_num))
    discovered_matchIds = utils.load_data('discovered_matchIds_' + str(checkpoint_num))
    g = utils.load_data('g_' + str(checkpoint_num))
    max_hop = utils.load_data('max_hop_' + str(checkpoint_num))
    bfs_queue = utils.load_data('bfs_queue_' + str(checkpoint_num))
    hop = utils.load_data('hop_' + str(checkpoint_num))
    print "Done loading."
    return matches, discovered_summonerIds, discovered_matchIds, g, max_hop, bfs_queue, hop


def save_state(checkpoint_num, matches, discovered_summonerIds, discovered_matchIds, g, max_hop, bfs_queue, hop):
    """
    Save all data structures to disk using a checkpoint num
    Args:
        checkpoint_num:
        matches:
        discovered_summonerIds:
        g:
        max_hop:
        bfs_queue:
        hop:

    Returns:
        no return
    """
    # Save state
    print "Saving state ..."
    utils.save_data(matches, 'matches_' + str(checkpoint_num))
    utils.save_data(discovered_summonerIds, 'discovered_summonerIds_' + str(checkpoint_num))
    utils.save_data(discovered_matchIds, 'discovered_matchIds_' + str(checkpoint_num))
    utils.save_data(g, 'g_' + str(checkpoint_num))
    utils.save_data(max_hop, 'max_hop_' + str(checkpoint_num))
    utils.save_data(bfs_queue, 'bfs_queue_' + str(checkpoint_num))
    utils.save_data(hop, 'hop_' + str(checkpoint_num))
    print "Done saving."

