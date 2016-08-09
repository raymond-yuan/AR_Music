import spotipy
import sys
import collections
import cPickle as pickle
from collections import defaultdict
import time

class Node:
    def __init__(self):
        self.pop_cost = 0
        self.g_cost = 0
        self.name = ''

    def __str__(self):
        return str(self.name)

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

    :param graph: Graph of {Artist_Name : {Artist(Node) : [{"Child": Child_Node}]}}
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

    start_node = graph[start_str].keys()[0]
    f_cost[start_str] = start_node.pop_cost

    while openset:

        min_f = min(f_cost.values())
        for key in f_cost:
            if f_cost[key] == min_f:
                node_name = key
            # print "KEY: ", key, key == end_str
        # print "FCOST", f_cost
        # print node_name
        if node_name == end_str:

            return reconstruct_path(parents, node_name)
        f_cost.pop(node_name)
        openset.remove(node_name)
        closedset.add(node_name)

        node = graph[node_name].keys()[0]
        for nbr in graph[node_name][node].keys():
            # print nbr
            if nbr in graph.keys():
                nbr_node = graph[nbr].keys()[0] # globals()[nbr]
                if nbr not in closedset and nbr not in openset:
                    openset.add(nbr)
                    nbr_node.g_cost = graph[node_name][node][nbr].rel_cost + node.g_cost
                    f_cost[nbr] = nbr_node.g_cost + nbr_node.pop_cost
                    parents[nbr] = node_name
                elif nbr in openset:
                    new_g = graph[node_name][node][nbr].rel_cost + node.g_cost
                    if new_g < nbr_node.g_cost:
                        nbr_node.g_cost = new_g
                        f_cost[nbr] = nbr_node.g_cost + nbr_node.pop_cost
                        parents[nbr] = node_name
                elif nbr in closedset:
                    continue
    return parents

def reconstruct_path(parents, current):
    total_path = [current]
    while current in parents.keys():
        current = parents[current]
        total_path.insert(0, current)
    return total_path

def bfs(start_artist):
    """
        Perform a breadth-first search on digraph graph starting at node startnode.

        Arguments:
        start_artist - String of your starting artist

        Returns:
        Graph of the whole shit nips
    """
    start_time = time.time()
    # graph_exp = defaultdict(lambda: {})
    graph_exp = defaultdict(lambda: defaultdict(lambda: {}))

    # name_p = process_name(start_artist)

    name_p = process_name(start_artist)

    # temp_node = Node()
    # temp_node.name = start_artist
    # temp_node.pop_cost = 0

    globals()[name_p] = Node()
    globals()[name_p].name = start_artist
    globals()[name_p].pop_cost = 0

    # Initialize search queue
    queue = collections.deque([globals()[name_p]])
    visited = set()

    count = 0
    # Loop until all connected nodes have been explored

    bad_list = []
    while queue:
        try:
            node = queue.popleft()
            # if count % 100 == 0:
            print count, node.name
            artist_info = spotify.search(q='artist:' + node.name, type='artist')
            if artist_info['artists']['items'] == []:
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
                    temp.name = artist["name"]
                    globals()[artist_name] = temp

                # Adds related artist to original node in graph
                temp_edge = Edge(artist['name'])
                temp_edge.rel_cost = i
                graph_exp[node.name][node][temp.name] = temp_edge
                i += 1

                if temp.name not in visited:
                    visited.add(temp.name)
                    queue.append(globals()[process_name(temp.name)])

            if count == 50:
                break

            # for nbr in graph_exp[node.name][node].keys():
            #     if nbr not in visited:
            #         visited.add(nbr)
            #         queue.append(globals()[process_name(nbr)])
            count += 1
        except:
            bad_list.append(node.name)
            print "Unexpected error:", sys.exc_info()[0], "at ", node.name


    for key in graph_exp.keys():
        graph_exp[key] = dict(graph_exp[key])

    text_file = open("broken_artist_list.txt", "w")
    text_file.write(str(bad_list))
    text_file.close()
    # pickle.dump(graph_exp, open(out_filename, "wb"))
    print time.time() - start_time
    return dict(graph_exp)


def astar_graph_gen(start_str):
    """

    :param graph: Graph of {Artist_Name : {Artist(Node) : [{"Child": Child_Node}]}}
    :param start_node: String of the Start Node
    :param end_node: String of the End Node
    :return: Parents Mapping (Path from Start Node to End Node )
    """
    start_time = time.time()
    openset = set([])
    closedset = set([])

    openset.add(start_str)

    graph_exp = defaultdict(lambda: defaultdict(lambda: {}))

    name_p = process_name(start_str)

    globals()[name_p] = Node()
    globals()[name_p].name = start_str
    globals()[name_p].pop_cost = 0

    count = 0
    bad_list = []
    while openset:
        try:
            node_name = openset.pop()
            node = globals()[process_name(node_name)]
            if count % 50 == 0:
                print count, node.name
            closedset.add(node_name)

            artist_info = spotify.search(q='artist:' + node_name, type='artist')
            if artist_info['artists']['items'] == []:
                closedset.add(node_name)
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
                    temp.name = artist["name"]
                    globals()[artist_name] = temp

                # Adds related artist to original node in graph
                temp_edge = Edge(artist['name'])
                temp_edge.rel_cost = i
                graph_exp[node.name][node][temp.name] = temp_edge
                i += 1

                if temp.name not in closedset:
                    openset.add(temp.name)
                    closedset.add(temp.name)
            count += 1
            # if count == 20:
            #     break
        except:

            bad_list.append(node.name)
            print "Unexpected error:", sys.exc_info()[0], "at ", node.name
    print end_time - start_time

    for key in graph_exp.keys():
        graph_exp[key] = dict(graph_exp[key])

    text_file = open("broken_artist_list.txt", "w")
    text_file.write(str(bad_list))
    text_file.close()
    # pickle.dump(graph_exp, open(out_filename, "wb"))
    print time.time() - start_time
    return dict(graph_exp)

def iddfs(start_artist):
    """
        Perform a iterative deepening depth first search on graph starting at node of name of st.

        Arguments:
        start_artist - String of your starting artist

        Returns:
        Graph of the whole shit nips
    """
    start_time = time.time()
    iddfs_graph_exp = defaultdict(lambda: defaultdict(lambda: {}))
    iddfs_visited = set()

    artist_info = spotify.search(q='artist:' + start_artist, type='artist')
    name_p = process_name(start_artist)
    globals()[name_p] = Node()
    globals()[name_p].name = artist_info['artists']['items'][0]['name']
    globals()[name_p].pop_cost = 0

    depth = 0
    while depth < 5:
        end = DLS(globals()[name_p], depth, iddfs_graph_exp,iddfs_visited)
        print 'Depth:', depth
        print '# of Artists:', len(iddfs_graph_exp)
        depth += 1
    for key in iddfs_graph_exp.keys():
        iddfs_graph_exp[key] = dict(iddfs_graph_exp[key])
    iddfs_graph_exp = dict(iddfs_graph_exp)
    end_time = time.time()
    print
    print start_time - end_time
    return iddfs_graph_exp


def DLS(node, depth, iddfs_graph_exp, iddfs_visited):
    if depth == 1:
        if len(iddfs_graph_exp.keys()) % 50 == 0:
            print len(iddfs_graph_exp.keys())

        if node.name not in iddfs_visited:
            iddfs_visited.add(node.name)
            artist_info = spotify.search(q='artist:' + node.name, type='artist')
            if artist_info['artists']['items'] == []:
                return
            uri = artist_info['artists']['items'][0]['uri']
            r_artists = spotify.artist_related_artists(uri)
            create_neighbors(node, r_artists, iddfs_graph_exp)

    if depth > 0:
        for nbr in iddfs_graph_exp[node.name][node].keys():
            DLS(globals()[process_name(nbr)], depth - 1, iddfs_graph_exp, iddfs_visited)

    return

def create_neighbors(node, related_artists, graph):
    i = 1
    for artist in related_artists['artists']:
        # Make related artist into a node
        artist_name = process_name(artist["name"])
        if artist_name not in globals():
            temp = Node()
            temp.pop_cost = 100 - artist['popularity']
            temp.name = artist["name"]
            globals()[artist_name] = temp
        # Adds related artist to original node in graph
        temp_edge = Edge(artist['name'])
        temp_edge.rel_cost = i
        graph[node.name][node][artist['name']] = temp_edge
        i += 1


# ye = Node()
# ye.name = 'ye'
# ye.pop_cost = 2

# bey = Edge('bey')
# bey.rel_cost = 3

# graphtest = defaultdict(lambda: {})
# graphtest[ye]['Bey'] = bey
# # graphtest = {ye:{'Bey':bey}}
# graphtest = dict(graphtest)
# print graphtest[ye]

# pickle.dump(graphtest, open("save.p", "wb"))

# graph_out = pickle.load(open("save.p", "rb"))

# print graph_out.keys()[0]
# # print graph_out[graph_out.keys()[0]]
# print

### GEN GRAPH AND WRTIE TO .P FILE ###
graph_out_bfs = astar_graph_gen("Kanye West")
pickle.dump(graph_out_bfs, open("BFS_Graph_Out.p", "wb"))

# graph_out_iddfs = bfs("Kanye West")
# pickle.dump(graph_out_iddfs, open("IDDFS_Graph_Out.p", "wb"))

BFS_Gen = pickle.load( open( "BFS_Graph_Out.p", "rb" ) )
print astar(BFS_Gen, "Kanye West", "Lil Wayne")

# IDDFS_Gen = pickle.load( open( "IDDFS_Graph_Out.p", "rb" ) )
# print astar(IDDFS_Gen,'Jeremih','Enrique Iglesias')

# {Name : {Node: {NAME EDGE: Edge}}}
