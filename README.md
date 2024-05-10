# SCOPE Optimal Routing

This repository must be opened in SCOPE. The directory must contain the following files in order to work:

- Administrative Boundaries
- europe.osm 

# Usage

To clone the code into the cluster, type the following command in SCOPE:

git clone https://github.com/metalforpc/SCOPE_Optimal_Routing/

# How the code works

The code is divided into phases:

- Phase 1: **Loading the Graph**

The script starts from main.py and calls the load_network function from the IO.py module. This function loads the Europe network from a pickle object, which contains motorways, trunk roads, and primary roads (and respective links). Once loaded, this object is stored in G.

- Phase 2: **Loading NUTS**

After loading the network's graph, the script calls the load_nuts function from the IO.py module. This function seeks the folder "Administrative Boundaries" and loads the NUTS shapefile. At this stage, the user can choose the NUTS level by using the CODE_LEVEL argument. The function loads the NUTS shapefile, extracts the corresponding NUTS code, computes centroids, and extracts the NUTS_ID for Italy (origins) and the NUTS_IDs for other countries (destinations). It returns the NUTS dataset, a list of origins, and destinations (in NUTS_ID format).

- Phase 3: **Adapting the NUTS geometry to G**

Once the graph and NUTS are loaded, the program extracts nodes and edges of the network from G. In doing so, we need to change the CRS specification of nodes and the graph to match that of the NUTS shapefile. This whole operation is performed by the get_nodes_edges_from_graph function called by the data_manipulation module.

- Phase 4: **Computing OD set**

Now that we have the nodes, edges, origins, and destinations in NUTS_ID, we have to transform the origins and destinations from NUTS_ID to actual nodes on the graph. To do so, we take the centroid of each NUTS and search for the nearest node in the graph. The od_nodes function takes care of this operation and once finished, returns a set of origin, destination nodes, and the Cartesian product of the two.

- Phase 5: **Optimal Routing**

Given all the information needed, the program computes the optimal routing from all origin to all destinations

- Phase 6: **Saving Results**

Saves the result and returns the dataframe
