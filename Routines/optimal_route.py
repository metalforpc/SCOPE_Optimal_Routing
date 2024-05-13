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
        return OD[0], OD[1], path
    except:
        logging.warning(f"Some error raised for {OD}")
        return OD[0], OD[1], [0]