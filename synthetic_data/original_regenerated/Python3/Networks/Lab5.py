
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
importmatplotlib.pyplotasplt
importnetworkxasnx
importgeopy.distance
fromoperatorimportitemgetter
NAME='Philo Decroos'
UVANETID='11752262'
defget_dist(G,node1,node2):
    """
    This function uses the geopy module to calculate the physical distance
    between two nodes of the network in kilometres, using their latitude
    and longitude coordinates.
    """
n1=G.nodes[node1]
n2=G.nodes[node2]
coor_1=(n1["Latitude"],n1["Longitude"])
coor_2=(n2["Latitude"],n2["Longitude"])
dist=geopy.distance.vincenty(coor_1,coor_2).km
returndist

deftask1a(G,source,dest):
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
vertices=[]
dist={}
prev={}
fornodeinG.nodes:
        dist[node]=float("inf")
prev[node]=None
vertices.append(node)
 dist[source]=0
whilevertices:
        min_node=""
smallest=float("inf")
forelinvertices:
            ifdist[el]<smallest:
                min_node=el
smallest=dist[el]
  vertices.remove(min_node)
ifdestisnotNoneandmin_node==dest:
            break
 neighbors=G.neighbors(min_node)
forneighborinneighbors:
            alt=dist[min_node]+get_dist(G,min_node,neighbor)
ifalt<dist[neighbor]:
                dist[neighbor]=alt
prev[neighbor]=min_node
   ifdestisNone:
        returnprev,dist
 path=[]
curr=dest
ifprev[curr]isnotNoneorcurr==source:
        whilecurrisnotNone:
            path.insert(0,curr)
curr=prev[curr]
  returnpath,round(dist[dest])

deftask1b(G):
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
nl_to_ie=task1a(G,'NL','IE')
nl_to_ch=task1a(G,'NL','CH')
ifnl_to_ie[1]>nl_to_ch[1]:
        longest=nl_to_ie
 else:
        longest=nl_to_ch
 returnlongest

deftask2a(G):
    """
    This method computes the diameter of a given network: the longest shortest
    path available in this network. It uses the algorithm from task1a.

    Parameters:
        G: the network of which we will compute the diameter.

    Returns:
        a tuple of the path that forms the diameter and its length in
        kilometres.
    """
paths=[]
fornodeinG.nodes:
        prev,dist=task1a(G,node,None)
dest=max(dist,key=dist.get)
length=dist[dest]
paths.append((length,node,dest))
 diameter=sorted(paths,key=itemgetter(0))[-1]
returntask1a(G,diameter[1],diameter[2])

deftask2b(G):
    """
    This function calls task2a to compute a diameter.

    Parameters:
        G: the network that will be used

    Returns:
        a tuple of the path that forms the diameter and its length in
        kilometres.
    """
returntask2a(G)

deffind_shortest_paths(G,lengths):
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
paths=[]
traversed=[]
fornode1inG.nodes:
        fornode2inG.nodes:
            if((node1,node2)intraversedor(node2,node1)intraversedornode1==node2):
                continue
 path,len=task1a(G,node1,node2)
iflengths:
                paths.append(len)
 else:
                paths.append(path)
 traversed.append((node1,node2))
  returnpaths

deftask3a(G):
    """
    This function computes the average of all shortest paths in a network.
    It uses the find_shortest_paths function to find the lengths of all the
    shortest paths and then computes the average.

    Parameters:
        G: the network of which the average shortest path will be computed

    Returns:
        The average of all shortest paths in G
    """
all_paths=find_shortest_paths(G,True)
average=0
forelinall_paths:
        average+=el
 average=average/len(all_paths)
returnaverage

deftask3b(G):
    """
    Uses task3a to find the average shortest path in a network.

    Parameters:
        G: the network

    Returns:
        The average of the shortest paths
    """
returntask3a(G)

deftask4a(G):
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
average=task3b(G)
smallest_avg=average
best_edge=None
checked=[]
fornode1inG.nodes:
        fornode2inG.nodes:
            if(node1==node2or(node1,node2)incheckedor(node2,node1)incheckedorG.has_edge(node1,node2)):
                continue
 G.add_edge(node1,node2)
new_avg=task3b(G)
G.remove_edge(node1,node2)
ifnew_avg<smallest_avg:
                smallest_avg=new_avg
best_edge=(node1,node2)
 checked.append((node1,node2))
  difference=average-smallest_avg
returnbest_edge[0],best_edge[1],round(difference)

deftask4b(G):
    """
    Uses task4a to find a most efficient new edge.

    Parameters:
        G: the network

    Returns:
        A tuple containing the names of the start and end node and the gain
        in average shortest path the adding of this edge would yield.
    """
returntask4a(G)

deftask5a(G):
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
centrality={}
shortest_paths=find_shortest_paths(G,False)
fornodeinG.nodes:
        centrality[node]=0
forpathinshortest_paths:
            ifpath[0]!=nodeandpath[-1]!=nodeandnodeinpath:
                centrality[node]+=1
   returncentrality

deftask5b(G):
    """
    This function finds the centrality of all nodes of G, and then finds the
    three most central nodes.

    Parameters:
        G: the network

    Returns:
        A list containing the names of the three most central nodes in G.
    """
centrality=task5a(G)
sorted_cent=list(reversed(sorted(centrality.items(),key=itemgetter(1))))
return[sorted_cent[0][0],sorted_cent[1][0],sorted_cent[2][0]]

if__name__=="__main__":
    G=nx.read_gml("topology1.gml")
G2=nx.read_gml("topology2.gml")
print('Networks and Network Security - Lab 5')
print('Name: {}'.format(NAME))
print('UvAnetID: {}'.format(UVANETID))
print()
print('Task 1')
print('b) {} ({} km)'.format(*task1b(G)))
print()
print('Task 2')
print('b) {} ({} km)'.format(*task2b(G)))
print()
print('Task 3')
print('b) {} km'.format(round(task3b(G2))))
print()
print('Task 4')
print('b) {} - {} ({} km)'.format(*task4b(G2)))
print()
print('Task 5')
print('b) 1. {}\n   2. {}\n   3. {}'.format(*task5b(G)))
print()

<EOF>