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
