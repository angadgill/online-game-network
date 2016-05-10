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

