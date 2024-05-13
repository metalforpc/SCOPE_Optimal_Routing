"""
This script loads the europe graph and save it as pickle serialized file.

To run this script use

python3 extract_europe.py --file=FILENAME

The file must be in the same directory 
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx as nx
import pickle
import logging
import argparse
from pathlib import Path

ox.settings.log_console=True
logging.getLogger().setLevel(logging.INFO)

HOME = Path(__file__).parent.parent

# Parser to use arguments when calling the script
parser = argparse.ArgumentParser(description="Compute Optimal Routings")
parser.add_argument("--file", required=True, type=str)
args = parser.parse_args()

file = args.file
path = f"{HOME}/Network/OSM/{file}.osm"

logging.warning("Loading Europe Graph")
G = ox.graph_from_xml(path)

logging.warning("Adding speeds and travel times")
G = ox.routing.add_edge_speeds(G)
G = ox.routing.add_edge_travel_times(G)

logging.warning("Exporting nodes and edges to geopandas dataframe")
nodes, edges = ox.graph_to_gdfs(G)
nodes.to_csv("nodes.csv")
edges.to_csv("edges.csv")

save_dir = f"{HOME}/Network/Serialized/{file}.gpickle"
logging.warning(f"Saving Graph in {save_dir}")
with open(save_dir, "wb") as f:
    pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)

logging.warning("Script Executed Correctly")