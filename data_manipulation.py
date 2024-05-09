import logging
import osmnx as ox
import numpy as np
import pandas as pd
import itertools


def get_nodes_edges_from_graph(G, NUTS):
    """
    Creates the nodes and edges geo-dataframe for the network
    and adjust the geometry according to NUTS.
    """
    # Create nodes and edges representation
    logging.info("Creating nodes and edges representation")
    nodes, edges = ox.graph_to_gdfs(G)
    logging.info("Created")

    # Rebuilding Geometry
    logging.info("Rebuilding Geometries")
    edges.to_crs(NUTS.crs, inplace=True)
    nodes.to_crs(NUTS.crs, inplace=True)
    logging.info("Geometries built correctly")

    return nodes, edges

def od_nodes(origins, destinations, NUTS, nodes):
    logging.info("Computing nearest origin node in the graph")

    origin_nodes = np.zeros(len(origins), dtype=int)

    for idx, origin in enumerate(origins):
        centroid = NUTS.loc[(NUTS.NUTS_ID == origin), 'centroids']
        origin_idx = nodes.geometry.sindex.nearest(centroid)[1][0]
        origin_nodes[idx] = int(nodes.iloc[origin_idx].name)

    destination_nodes = np.zeros(len(destinations), dtype=int)
    for idx, dest in enumerate(destinations):
        centroid = NUTS.loc[(NUTS.NUTS_ID == dest), 'centroids']
        dest_idx = nodes.geometry.sindex.nearest(centroid)[1][0]
        destination_nodes[idx] = int(nodes.iloc[dest_idx].name)

    od_set = list(itertools.product(origin_nodes, destination_nodes))
    
    return origin_nodes, destination_nodes, od_set



def create_output_dataframe(nrows, paths=5):
    """
    Create an empty dataframe properly formatted for the output
    """

    # Base Columns and dtypes
    columns = ["FROM", "TO", "FROM_NODE", "TO_NODE", "FROM_NAME", "TO_NAME"]
    types = {"FROM":float, "TO":float, "FROM_NODE":int, "TO_NODE":int, "FROM_NAME":str, "TO_NAME":str}

    # Create columns and types for any paths
    for path in range(1,paths+1):
        columns.append(f"PATH_{path}")
        types[f"PATH_{path}"] = object

    df = pd.DataFrame(columns=columns, index=range(0, nrows))
    df = df.astype(types)

    return df

