import osmnx as ox
import networkx as nx
import logging

def compute_single_dijkstra(G, OD):
    """
    Given a graph and an origin destination couple, compute the shortest path.
    If any error is raised, the function returns 0
    """
    try:
        logging.info(f"Computing shortest path for {OD}")
        path = nx.dijkstra_path(G, source=OD[0], target=OD[1], weight="travel_time")
        logging.info(f"Shortest path for {OD} computed")
    except:
        logging.warning(f"Some error raised for {OD}")
        return 0
    
    return path 

def compute_optimal_route(G, NUTS, nodes, origin_node, country, k_paths = 5):

    try:
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