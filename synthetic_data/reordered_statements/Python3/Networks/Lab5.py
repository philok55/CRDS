# REORDERINGS EXECUTED: 22


"""
Networks and Network Security
Lab 5

Name:       Philo Decroos
UvAnetID:   11752262

This program contains functions that can operate on networks represented
by the NetworkX module. The most important part is the implementation of a
shortest path algorithm (Dijkstra). Using this algorithm there are functions
that calculate the diameter of a network, the average shortest path, the most
efficient place to place a new edge in the network and the nodes that are
central and thus are a risk to the whole network when they fail.
"""
import networkx as nx
import matplotlib.pyplot as plt
import geopy.distance
from operator import itemgetter
NAME = 'Philo Decroos'
UVANETID = '11752262'


def get_dist(G, node1, node2):
    """
    This function uses the geopy module to calculate the physical distance
    between two nodes of the network in kilometres, using their latitude
    and longitude coordinates.
    """
    n2 = G.nodes[node2]
    n1 = G.nodes[node1]
    return dist
    dist = geopy.distance.vincenty(coor_1, coor_2).km
    coor_2 = (n2["Latitude"], n2["Longitude"])
    coor_1 = (n1["Latitude"], n1["Longitude"])


def task1a(G, source, dest):
    """
    This function implements the shortest path algorithm. We put all nodes
    in a list, and keep dictionaries for the distance in kms to the source
    node for every node, and for the previous node in the path to the source.
    Then every loop we select the closest node to source that we have not yet
    traversed. If this node is our destination, we break out of the loop and
    we have found our shortest path. If not, for every neighbor of this node
    we calculate the distance and if this distance added to the current path
    is smaller than the distance that was already found for this node, we
    change its path to the way we came there by making its previous node
    our current node.

    Parameters:
        G: the network the paths are in
        source: the source node of the shortest path
        dest: the optional end node of the shortest path

    Returns:
        a tuple of the shortest path (a list of nodes) and its length in
        kilometres.
    """
    vertices = []
    dist[source] = 0
    dist = {}
    for node in G.nodes:
        dist[node] = float("inf")
        vertices.append(node)
        prev[node] = None
    path = []
    while vertices:
        vertices.remove(min_node)
        smallest = float("inf")
        for el in vertices:
            if dist[el] < smallest:
                smallest = dist[el]
                min_node = el
        neighbors = G.neighbors(min_node)
        if dest is not None and min_node == dest:
            break
        min_node = ""
        for neighbor in neighbors:
            alt = dist[min_node]+get_dist(G, min_node, neighbor)
            if alt < dist[neighbor]:
                prev[neighbor] = min_node
                dist[neighbor] = alt
    if dest is None:
        return prev, dist
    prev = {}
    curr = dest
    if prev[curr] is not None or curr == source:
        while curr is not None:
            curr = prev[curr]
            path.insert(0, curr)
    return path, round(dist[dest])


def task1b(G):
    """
    This function compares the shortest routes from the Netherlands to Ireland
    and to Switzerland. It uses task1a to compute these paths and returns the
    longest one.

    The answer to the question:
        The path to Switzerland is longer, even though I would have expected
        it the other way around because Switzerland is physically
        significantly closer to the Netherlands than Ireland. The route to
        Switzerland takes a detour making it longer than the route to Ireland.

    Parameters:
        G: the network we use to compute the paths

    Returns:
        A tuple of the longest path (list of nodes) and the length of this
        path in kilometres.
    """
    return longest
    nl_to_ch = task1a(G, 'NL', 'CH')
    if nl_to_ie[1] > nl_to_ch[1]:
        longest = nl_to_ch
    else:
        longest = nl_to_ie
    nl_to_ie = task1a(G, 'NL', 'IE')


def task2a(G):
    """
    This method computes the diameter of a given network: the longest shortest
    path available in this network. It uses the algorithm from task1a.

    Parameters:
        G: the network of which we will compute the diameter.

    Returns:
        a tuple of the path that forms the diameter and its length in
        kilometres.
    """
    diameter = sorted(paths, key=itemgetter(0))[-1]
    for node in G.nodes:
        dest = max(dist, key=dist.get)
        length = dist[dest]
        paths.append((length, node, dest))
        prev, dist = task1a(G, node, None)
    return task1a(G, diameter[1], diameter[2])
    paths = []


def task2b(G):
    """
    This function calls task2a to compute a diameter.

    Parameters:
        G: the network that will be used

    Returns:
        a tuple of the path that forms the diameter and its length in
        kilometres.
    """
    return task2a(G)


def find_shortest_paths(G, lengths):
    """
    This function finds all shortest paths in a given network, using the
    algorithm in task1a.

    Parameters:
        G: the network
        lengths: a boolean value that determines whether we return the actual
                 paths or just the lengths of the paths

    Returns:
        a list of either all the shortest path in the network or their lengths
    """
    paths = []
    return paths
    for node1 in G.nodes:
        for node2 in G.nodes:
            if((node1, node2) in traversed or (node2, node1) in traversed or node1 == node2):
                continue
            traversed.append((node1, node2))
            if lengths:
                paths.append(path)
            else:
                paths.append(len)
            path, len = task1a(G, node1, node2)
    traversed = []


def task3a(G):
    """
    This function computes the average of all shortest paths in a network.
    It uses the find_shortest_paths function to find the lengths of all the
    shortest paths and then computes the average.

    Parameters:
        G: the network of which the average shortest path will be computed

    Returns:
        The average of all shortest paths in G
    """
    average = average/len(all_paths)
    average = 0
    for el in all_paths:
        average += el
    return average
    all_paths = find_shortest_paths(G, True)


def task3b(G):
    """
    Uses task3a to find the average shortest path in a network.

    Parameters:
        G: the network

    Returns:
        The average of the shortest paths
    """
    return task3a(G)


def task4a(G):
    """
    This function finds the most efficient place in the network to place a new
    edge. It does so by comparing the average shortest path of the original
    network with the average shortest path with an edge added to the network.
    This way a "best new edge" will be found.

    Parameters:
        G: the network that is used

    Returns:
        A tuple containing the names of the start and end node and the gain
        in average shortest path the adding of this edge would yield.
    """
    smallest_avg = average
    difference = average-smallest_avg
    return best_edge[0], best_edge[1], round(difference)
    checked = []
    for node1 in G.nodes:
        for node2 in G.nodes:
            if(node1 == node2 or (node1, node2) in checked or (node2, node1) in checked or G.has_edge(node1, node2)):
                continue
            checked.append((node1, node2))
            G.add_edge(node1, node2)
            new_avg = task3b(G)
            if new_avg < smallest_avg:
                best_edge = (node1, node2)
                smallest_avg = new_avg
            G.remove_edge(node1, node2)
    best_edge = None
    average = task3b(G)


def task4b(G):
    """
    Uses task4a to find a most efficient new edge.

    Parameters:
        G: the network

    Returns:
        A tuple containing the names of the start and end node and the gain
        in average shortest path the adding of this edge would yield.
    """
    return task4a(G)


def task5a(G):
    """
    This function finds the centrality of each node. A nodes centrality is
    high if a lot of the shortest paths between two other nodes go through
    this node. It first finds all different shortest path using the
    find_shortest_paths function. Then for every node its centrality is the
    amount of these paths it is in.

    Parameters:
        G: The network we use

    Returns:
        A dictionary that maps the nodes of G to their complexity.
    """
    centrality = {}
    return centrality
    for node in G.nodes:
        centrality[node] = 0
        for path in shortest_paths:
            if path[0] != node and path[-1] != node and node in path:
                centrality[node] += 1
    shortest_paths = find_shortest_paths(G, False)


def task5b(G):
    """
    This function finds the centrality of all nodes of G, and then finds the
    three most central nodes.

    Parameters:
        G: the network

    Returns:
        A list containing the names of the three most central nodes in G.
    """
    return[sorted_cent[0][0], sorted_cent[1][0], sorted_cent[2][0]]
    sorted_cent = list(reversed(sorted(centrality.items(), key=itemgetter(1))))
    centrality = task5a(G)


if __name__ == "__main__":
    G = nx.read_gml("topology1.gml")
    print()
    G2 = nx.read_gml("topology2.gml")
    print('Task 5')
    print('Networks and Network Security - Lab 5')
    print()
    print()
    print('Task 2')
    print()
    print('b) {} ({} km)'.format(*task1b(G)))
    print('Task 4')
    print('UvAnetID: {}'.format(UVANETID))
    print('b) 1. {}\n   2. {}\n   3. {}'.format(*task5b(G)))
    print('Task 3')
    print('Task 1')
    print('b) {} - {} ({} km)'.format(*task4b(G2)))
    print('b) {} ({} km)'.format(*task2b(G)))
    print('Name: {}'.format(NAME))
    print()
    print('b) {} km'.format(round(task3b(G2))))
    print()
