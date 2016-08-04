import spotipy
import sys

class Node:
    def _init_(self):
        self.pop_cost = 0
        self.name = ''

    def __str__(self):
        return str(Node)

class Edge:
    def _init_(self, node2):
        self.child = node2
        self.rel_cost = 0

graph = {}
used = set([])

if len(sys.argv) > 1:
    input = sys.argv[1]
else:
    input = 'Kanye West'

spotify = spotipy.Spotify()
artist_info = spotify.search(q='artist:' + input, type='artist')

name = artist_info['artists']['items'][0]['name']
uri = artist_info['artists']['items'][0]['uri']
r_artists = spotify.artist_related_artists(uri)

def process_name(in_string):
    name_p = ""
    for c in in_string:
        if c == " ":
            name_p += "_"
        else:
            name_p += c
    return name_p

name_p = process_name(name)

globals()[name_p] = Node()
globals()[name_p].name = name
graph[globals()[name_p]] = []

i=0
for artist in r_artists['artists']:
    temp = Node()
    temp.pop_cost = artist['popularity']
    temp.name = artist['name']
    artist_name = process_name(artist["name"])
    globals()[artist_name] = temp
    graph[globals()[name_p]].append(globals()[artist_name])
    i += 1

for art in graph[globals()[name_p]]:
    print art.name, art.pop_cost


