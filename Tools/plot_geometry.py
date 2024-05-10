import IO
import data_manipulation
import matplotlib.pyplot as plt

import logging
logging.getLogger().setLevel(logging.INFO)

# Load network and convert geometry
G = IO.load_network()
NUTS, origins_nuts, destinations_nuts, OD_names = IO.load_nuts()
nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

logging.info("Creating plot")
fig, ax = plt.subplots(figsize=(20,10))

logging.info("Plotting edges")
edges.plot(ax = ax, color='black', alpha=0.2)

logging.info("Plotting EU geometries")
NUTS.plot(ax = ax)
NUTS.centroids.plot(ax = ax, color='red')
plt.axis('off')

logging.info("Saving file to output")
fig.savefig("output.png")
logging.info("End of the script...")