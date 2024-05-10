"""
This script loads the europe graph and save it as pickle serialized file.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx as nx
import pickle
import logging

ox.settings.log_console=True

logging.warning("Loading Europe Graph")
G = ox.graph_from_xml("Europe.osm")

logging.warning("Adding speeds and travel times")
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

logging.warning("Exporting nodes and edges to geopandas dataframe")
nodes, edges = ox.graph_to_gdfs(G)
nodes.to_csv("nodes.csv")
edges.to_csv("edges.csv")

logging.warning("Saving Graph")
with open("Europe_Graph.gpickle", "wb") as f:
    pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)

logging.warning("Script Executed Correctly")