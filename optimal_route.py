import osmnx as ox
import logging

def compute_optimal_route(G, NUTS, nodes, origin_node, country, k_paths = 5):

    logging.info(f"Getting destination Node")
    dest_idx = nodes.geometry.sindex.nearest(NUTS[NUTS.CNTR_CODE == country].centroids)
    dest_node = nodes.iloc[dest_idx].name
    
    logging.info(f"Shortest path for {country}")
    paths = ox.routing.k_shortest_paths(G, origin_node, dest_node, k_paths, weight="travel_time")
    paths = list(paths)
    return paths