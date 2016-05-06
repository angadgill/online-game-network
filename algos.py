"""
All algorithms and functions are written here

Author: Angad Gill
"""

import networkx as nx


def add_clique_with_weights(graph, nodes, edge_attr=None):
    """
    Creates a clique between nodes. Creates undirected edges with weight=1.
    Adds weight to edges if they already exist.

    Parameters:
        graph: NetworkX graph data structure
        nodes: list of nodes
        edge_attr:
    Return:
        graph: NetworkX graph data structure with added clique
    """
    graph.add_nodes_from(nodes)

    num_nodes = len(nodes)

    # Create all combinations of nodes
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):  # No self-edges
            node1 = nodes[i]
            node2 = nodes[j]
            if graph.has_edge(node1, node2):
                # Add weight if edge exists
                graph.edge[node1][node2]['weight'] += 1
            else:
                # Create a new edge if it doesn't exist
                graph.add_edge(node1, node2, weight=1)

    return graph


def normalize(numbers):
    """
    Normalize a numpy array using mean-center and std-scale.

    Parameters:
        numbers: numpy array
    Return:
        numbers: normalized numpy array
    """
    numbers = (numbers - np.mean(numbers))/np.std(numbers)
    return numbers


def generate_team_graph(challenges):
    """
    Generate a NetworkX graph based on data from a list of Challenges
    :param challenges: list of dicts containing Challenge data
    :return: networkx graph
    """
    # Create a graph of all characters as nodes
    # and number of challanges on leaderboard as edges
    g = nx.Graph()

    for challenge in challenges:
        for group in challenge['groups']:
            names = []  # List of node names to add to graph
            for member in group['members']:
                if member.has_key('character'):  # Only add if character info is available
                    name = member['character']['name']
                    #                 print name
                    names += [name]
                    #         print names
            g = add_clique_with_weights(g, names)

    return g


def get_metrics(challenges, graph):
    """
    For a given network of characters and list of challenges completed by these characters, this function computes the
    algebraic connectivity for each group that played together and extracts the time taken by the team to complete
    challenge.

    :param:
        challenges: list of dict containing Challenge info
        graph: NetworkX graph of characters
    :return:
        tuple of two lists: algebraic connectivity and Challenge completion time
    """
    ac = []
    time = []

    for challenge in challenges:
        for group in challenge['groups']:
            names = []  # List of node names to add to graph
            for member in group['members']:
                if member.has_key('character'):  # Only add if character info is available
                    name = member['character']['name']
                    names += [name]

            g_team = graph.subgraph(names)
            if len(g_team.nodes()) > 1:
                ac += [nx.algebraic_connectivity(g_team)]
                time += [group['time']['time']]
    return ac, time