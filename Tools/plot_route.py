import sys
import os
from pathlib import Path

# Absolute path for import "Routines Modules"
path = Path(__file__).parent.parent
sys.path.append(os.path.abspath(path))

from Routines import IO
from Routines import data_manipulation
import matplotlib.pyplot as plt

# Logger
import logging
logging.getLogger().setLevel(logging.INFO)

# Load network and convert geometry
G = IO.load_network()
NUTS, origins_nuts, destinations_nuts, OD_names = IO.load_nuts()
nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

res = IO.load_results("NUTS_1")

logging.info("Creating plot")
fig, ax = plt.subplots(figsize=(20,10))

logging.info("Plotting edges")
edges.plot(ax = ax, color='black', alpha=0.2)

logging.info("Plotting EU geometries")
NUTS.plot(ax = ax)
NUTS.centroids.plot(ax = ax, color='red')

nodes[nodes.index.isin(res[1][2])].plot(ax = ax, color='green')

ax.set_xlim([0.25*1e7, 0.75*1e7])
ax.set_ylim([1*1e6, 6.8*1e6])
plt.axis('off')

logging.info("Saving file to output")
fig.savefig(f"{path}/Outputs/Figures/Optimal_Route.png")
logging.info("End of the script...")