"""
All algorithms and functions are written here

Author: Angad Gill
"""


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