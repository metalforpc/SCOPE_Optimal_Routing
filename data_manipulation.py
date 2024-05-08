import logging
import osmnx as ox

def get_nodes_edges_from_graph(G, NUTS):
    """
    Creates the nodes and edges geo-dataframe for the network
    and adjust the geometry according to NUTS.
    """
    # Create nodes and edges representation
    logging.warning("Creating nodes and edges representation")
    nodes, edges = ox.graph_to_gdfs(G)
    logging.warning("Created")

    # Rebuilding Geometry
    logging.warning("Rebuilding Geometries")
    edges.to_crs(NUTS.crs, inplace=True)
    nodes.to_crs(NUTS.crs, inplace=True)
    logging.warning("Geometries built correctly")

    return nodes, edges