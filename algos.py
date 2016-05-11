"""
All algorithms and functions are written here

Author: Angad Gill
"""

import networkx as nx
import utils


def add_clique_with_weights(graph, nodes, edge_attr=None):
    """
    Creates a clique between nodes. Creates undirected edges with weight=1.
    Adds weight to edges if they already exist. It also appends edge attributes
    such that the values form a list.

    Parameters:
        graph: NetworkX graph data structure
        nodes: list of nodes
        edge_attr: dict containing edge attributes
    Return:
        graph: NetworkX graph data structure with added clique
    """

    # Add all nodes to graph
    graph.add_nodes_from(nodes)

    num_nodes = len(nodes)

    # Add all combinations of edges, to form a clique
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):  # No self-edges
            node1 = nodes[i]
            node2 = nodes[j]
            if graph.has_edge(node1, node2):
                edge = graph.edge[node1][node2]

                # Add weight if edge exists
                edge['weight'] += 1

                # Append edge_attr values to the edge

                if edge_attr is not None:
                    for key in edge_attr.keys():
                        # TODO: Remove this check and figure out why edge_attr sometimes has 'weight' in it
                        if key == 'weight':
                            continue
                        if type(edge[key]) is list:
                            edge[key] += [edge_attr[key]]
                        else:
                            edge[key] = [edge[key], edge_attr[key]]

            else:
                # Create a new edge if it doesn't exist
                graph.add_edge(node1, node2, weight=1, attr_dict=edge_attr)

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


def get_metrics(challenges, graph, ac_metric= True, time_metric=True, degree_metrics=False):
    """
    For a given network of characters and list of challenges completed by these characters, this function computes the
    algebraic connectivity for each group that played together and extracts the time taken by the team to complete
    challenge.

    :param:
        challenges: list of dict containing Challenge info
        graph: NetworkX graph of characters
        ac_metric: Boolean. Default True. Function returns algebraic connectivity if set to True.
        time_metric: Boolean. Default True. Function returns challenge completion time if set to True.
        degree_metrics: Boolean. Default False. Function returns
    :return:
        tuple of two lists: algebraic connectivity and Challenge completion time
    """
    if ac_metric:
        ac = []
    if time_metric:
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
                if ac_metric:
                    ac += [nx.algebraic_connectivity(g_team)]
                if time_metric:
                    time += [group['time']['time']]
    # r =
    return ac, time