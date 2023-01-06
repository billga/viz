import json
import networkx as nx
from pyvis.network import Network

# constants
STATIC_PATH_PREFIX = "html/"
BACKGROUND_COLOR = "#222222"
EDGE_COLOR = "#ED8537"
FONT_COLOR = "white"
SERVICE_NODE_COLOR = "cyan"
OTHER_NODE_COLOR = "orange"
SERVICE_NODE_SIZE = 15
OTHER_NODE_SIZE = 25
HEADING = "PyViz for Kicks"


# Utils
def add_node(di_graph, node1, node2):
    di_graph.add_node(node2)
    edge = (node1, node2)
    di_graph.add_edge(*edge, color=EDGE_COLOR)


def process_nodes(di_graph, filename):
    g = Network(
        height=800,
        width=1400,
        directed=True,
        bgcolor=BACKGROUND_COLOR,
        font_color=FONT_COLOR,
        heading=HEADING,
    )
    g.repulsion(node_distance=100, central_gravity=0.2, spring_length=200, spring_strength=0.05, damping=0.09)
    # g.hrepulsion(node_distance=200, central_gravity=0.10, spring_length=150, spring_strength=0.01, damping=0.5)
    g.show_buttons(filter_=["physics"])  # ["physics", "interaction"]
    g.inherit_edge_colors(False)
    g.from_nx(di_graph)
    g.save_graph(STATIC_PATH_PREFIX + filename)
    # g.save_graph("../"+filename)


# Generators
def gen_graph(data):
    G = nx.DiGraph()
    nodes = data.keys()
    for service in nodes:
        G.add_node(service.lower())
        for item in data.get(service).get("related", []):
            add_node(G, service, item)
    process_nodes(G, "graph.html")


def gen_artists(data):
    """ this data looks different: dict (nodes) of lists (nodes) """
    G = nx.DiGraph()
    nodes = data.keys()
    for artist in nodes:
        G.add_node(artist)
        for item in data[artist]:
            add_node(G, artist, item)
    process_nodes(G, "artist.html")


if __name__ == '__main__':
    with open("graph.json", "r") as f:
        dep_data = json.load(f)
    gen_graph(dep_data)

    with open('artists.json', 'r') as f:
        art_data = json.load(f)
    gen_artists(art_data)


