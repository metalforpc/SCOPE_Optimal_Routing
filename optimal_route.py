import osmnx as ox
import networkx as nx
import logging

def compute_optimal_route(G, NUTS, nodes, origin_node, country, k_paths = 5):
    try:
        logging.info(f"Getting destination Node")
        dest_idx = nodes.geometry.sindex.nearest(NUTS[NUTS.CNTR_CODE == country].centroids)[1][0]
        dest_node = nodes.iloc[dest_idx].name
        
        logging.info(f"Shortest path for {country}")
        #paths = ox.routing.k_shortest_paths(G, origin_node, dest_node, k_paths, weight="travel_time")
        #paths = list(paths)
        path = nx.dijkstra_path(G, source=origin_node, target=dest_node, weight="travel_time")
        logging.info(f"Shortest path for {country} computed")
    except:
        logging.warning(f"Some error for {country}")
        return 0
    return path