import spotipy
import sys
import collections
from collections import defaultdict

class Node:
    def __init__(self):
        self.pop_cost = 0
        self.g_cost = 0
        self.name = ''

    def __str__(self):
        return str(Node)

class Edge:
    # node to is the string *make sure to make it a processed name
    def __init__(self, node2):
        self.child = node2
        self.rel_cost = 0

graph = {}
used = set([])

if len(sys.argv) > 1:
    input = sys.argv[1]
else:
    input = 'Kanye West'
#
spotify = spotipy.Spotify()
# artist_info = spotify.search(q='artist:' + input, type='artist')
#
# name = artist_info['artists']['items'][0]['name']
# uri = artist_info['artists']['items'][0]['uri']
# r_artists = spotify.artist_related_artists(uri)

def process_name(in_string):
    return in_string.replace(' ','_')

# name_p = process_name(name)
#
# globals()[name_p] = Node()
# globals()[name_p].name = name
# graph[globals()[name_p]] = {}

# i=0
# for artist in r_artists['artists']:
#     temp = Node()
#     temp.pop_cost = 100 - artist['popularity']
#     temp.name = artist['name']
#     artist_name = process_name(artist["name"])
#
#     temp_edge = Edge(artist_name)
#     temp_edge.rel_cost = i
#     globals()[artist_name] = temp
#     graph[globals()[name_p]][artist_name] = temp_edge
#     i += 1
#
# for art in graph[globals()[name_p]]:
#     print art
#
# print graph

def astar(graph, start_str, end_str):
    """

    :param graph: Graph of {Artist(Node) : [{"Child": Child_Node}]}
    :param start_node: String of the Start Node
    :param end_node: String of the End Node
    :return: Parents Mapping (Path from Start Node to End Node )
    """

    f_cost = {}
    parents = {}
    openset = set([])
    closedset = set([])
    parents[start_str] = None
    openset.add(start_str)

    start_node = globals()[start_str]
    f_cost[start_str] = start_node.pop_cost

    while openset:

        min_f = min(f_cost.values())
        for key in f_cost:
            if f_cost[key] == min_f:
                node_name = key
        if node_name == end_str:
            return parents
        f_cost.pop(node_name)

        openset.remove(node_name)
        closedset.add(node_name)

        node = globals()[node_name]
        for nbr in graph[node].keys():
            nbr_node = globals()[nbr]
            if nbr not in closedset and nbr not in openset:
                openset.add(nbr)
                nbr_node.g_cost = graph[node][nbr].rel_cost + node.g_cost
                f_cost[nbr] = nbr_node.g_cost + nbr_node.pop_cost
                parents[nbr] = node_name
            elif nbr in openset:
                new_g = graph[node][nbr].rel_cost + node.g_cost
                if new_g < nbr_node.g_cost:
                    nbr_node.g_cost = new_g
                    f_cost[nbr] = nbr_node.g_cost + nbr_node.pop_cost
                    parents[nbr] = node_name
            elif nbr in closedset:
                continue

    return parents



def bfs(start_artist):
    """
        Perform a breadth-first search on digraph graph starting at node startnode.

        Arguments:
        start_artist - String of your starting artist

        Returns:
        Graph of the whole shit nips
    """
    graph_exp = defaultdict(lambda: {})

    # artist_info = spotify.search(q='artist:' + start_artist, type='artist')
    # name = artist_info['artists']['items'][0]['name']
    # uri = artist_info['artists']['items'][0]['uri']
    # r_artists = spotify.artist_related_artists(uri)

    name_p = process_name(start_artist)

    globals()[name_p] = Node()
    globals()[name_p].name = start_artist
    globals()[name_p].pop_cost = 0

    # Initialize search queue
    queue = collections.deque([globals()[name_p]])
    visited = set()

    # Loop until all connected nodes have been explored
    while queue:
        node = queue.popleft()

        artist_info = spotify.search(q='artist:' + node.name, type='artist')
        if (artist_info['artists']['items'] == []):
            visited.add(node.name)
            continue
        # name = artist_info['artists']['items'][0]['name']
        uri = artist_info['artists']['items'][0]['uri']
        r_artists = spotify.artist_related_artists(uri)

        i = 1
        for artist in r_artists['artists']:
            # Make related artist into a node
            artist_name = process_name(artist["name"])
            if artist_name not in globals():
                temp = Node()
                temp.pop_cost = 100 - artist['popularity']
                temp.name = artist['name']
                globals()[artist_name] = temp

            # Adds related artist to original node in graph
            temp_edge = Edge(artist_name)
            temp_edge.rel_cost = i
            graph_exp[node][artist_name] = temp_edge
            i += 1

        for nbr in graph_exp[node].keys():
            if nbr not in visited:
                visited.add(nbr)
                queue.append(globals()[nbr])
        print graph_exp
    return graph_exp

# print bfs("Kanye West")

def iddfs(start_artist):
    """
        Perform a iterative deepening depth first search on graph starting at node of name of st.

        Arguments:
        start_artist - String of your starting artist

        Returns:
        Graph of the whole shit nips
    """
    iddfs_graph_exp = defaultdict(lambda: {})

    # artist_info = spotify.search(q='artist:' + start_artist, type='artist')
    # name = artist_info['artists']['items'][0]['name']
    # uri = artist_info['artists']['items'][0]['uri']
    # r_artists = spotify.artist_related_artists(uri)

    name_p = process_name(start_artist)

    globals()[name_p] = Node()
    globals()[name_p].name = start_artist
    globals()[name_p].pop_cost = 0

    while true:
        depth = 0
        end = DLS(globals()[name_p],depth)
        if end:
            break
        depth+=1

def DLS(node, depth):
    if depth > 0:
        artist_info = spotify.search(q='artist:' + node.name, type='artist')
        # name = artist_info['artists']['items'][0]['name']
        uri = artist_info['artists']['items'][0]['uri']
        r_artists = spotify.artist_related_artists(uri)
        i = 1
        for artist in r_artists['artists']:
            artist_name = process_name(artist["name"])
            if artist_name not in globals():
                temp = Node()
                temp.pop_cost = 100 - artist['popularity']
                temp.name = artist['name']
                globals()[artist_name] = temp

            # Adds related artist to original node in graph
            temp_edge = Edge(artist_name)
            temp_edge.rel_cost = i
            iddfs_graph_exp[node][artist_name] = temp_edge
            i += 1

        for nbr in iddfs_graph_exp[node].keys():
            found = DLS(globals()[nbr], depth - 1)
            if found is None:
                return false
    return true

ye = Node()
ye.name = 'ye'
ye.pop_cost = 2
bey = Edge('bey')
bey.rel_cost = 3
graphtest = {ye:{'Bey':bey}}
text_file = open("Output.txt","w")
text_file.write(graphtest)
text_file.close()