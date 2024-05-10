from . import IO
from . import data_manipulation
import matplotlib.pyplot as plt

# Load network and convert geometry
G = IO.load_network()
NUTS, origins_nuts, destinations_nuts, OD_names = IO.load_nuts()
nodes, edges = data_manipulation.get_nodes_edges_from_graph(G, NUTS)

fig, ax = plt.subplots(figsize=(20,10))
edges.plot(ax = ax, color='black', alpha=0.2)
NUTS.plot(ax = ax)
NUTS.centroids.plot(ax = ax, color='red')
plt.axis('off')
fig.savefig("output.png")